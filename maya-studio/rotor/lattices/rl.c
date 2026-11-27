// Rotor-router aggregation / IDLA on three lattices.
// usage: rl lattice mode n seed [dump]
// lattice 0: square clockwise N E S W, 1: square N S E W, 2: triangular (axial, 6 dirs clockwise), 3: honeycomb (brick wall, 3 dirs)
// mode 0: all arrows start at direction 0; 1: random start; 2: IDLA
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define W 1201
#define C (W/2)
static unsigned char occ[W*W], rot[W*W];
static uint64_t s;
static inline uint64_t rng(){ s^=s<<13; s^=s>>7; s^=s<<17; return s; }
static int lat;
static const double S3=1.7320508075688772;
static void pos(int x,int y,double*px,double*py){
  int a=x-C,b=y-C;
  if(lat<=1){*px=a;*py=b;}
  else if(lat==2){*px=a+0.5*b;*py=b*S3/2;}
  else {*px=a*S3/2; *py=1.5*b+((((a+b)%2)+2)%2==0?0.0:-0.5);} 
}
int main(int argc,char**argv){
  lat=atoi(argv[1]); int mode=atoi(argv[2]); long n=atol(argv[3]); s=atol(argv[4])*2654435761ULL+88172645463325252ULL;
  int nd = lat<=1?4:(lat==2?6:3);
  double area = lat<=1?1.0:(lat==2?S3/2:3*S3/4);
  // square cw: N E S W ; square NSEW ; tri axial clockwise starting east: E, SE(1,-1)... use (1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)
  int sdx[4]={0,1,0,-1}, sdy[4]={1,0,-1,0};
  int ndx[4]={0,0,1,-1}, ndy[4]={1,-1,0,0};
  int tdx[6]={1,1,0,-1,-1,0}, tdy[6]={0,-1,-1,0,1,1};
  for(int i=0;i<W*W;i++) { rot[i]= mode==1 ? (unsigned char)(rng()%nd) : 0; if(mode>=3){int x=i%W-C,y=i/W-C; if((((x+y)%2)+2)%2) rot[i]=mode-2;} }
  double rout2=0; long steps=0; double sumx2=0, sx=0, sy=0; long next=100;
  for(long k=1;k<=n;k++){
    int x=C,y=C;
    while(occ[y*W+x]){
      int i=y*W+x; int d;
      if(mode==2) d=rng()%nd; else { rot[i]=(rot[i]+1)%nd; d=rot[i]; }
      if(lat==0){x+=sdx[d];y+=sdy[d];}
      else if(lat==1){x+=ndx[d];y+=ndy[d];}
      else if(lat==2){x+=tdx[d];y+=tdy[d];}
      else { int A=((((x-C)+(y-C))%2)+2)%2==0; // A: vertical bond up
        // clockwise from vertical: A: up, right-down, left-down ; B: down, left-up, right-up
        if(A){ if(d==0) y++; else if(d==1) x++; else x--; }
        else { if(d==0) y--; else if(d==1) x--; else x++; } }
      steps++;
      if(x<1||x>=W-1||y<1||y>=W-1){fprintf(stderr,"escaped\n");return 1;}
    }
    occ[y*W+x]=1;
    double px,py; pos(x,y,&px,&py); double r2=px*px+py*py; sumx2+=r2; sx+=px; sy+=py; if(r2>rout2) rout2=r2;
    if(k==next||k==n){
      double rin2=1e18; int R=(int)(sqrt(rout2)*1.3)+3; double cx=sx/k, cy=sy/k, co2=0, ci2=1e18;
      for(int yy=C-R;yy<=C+R;yy++)for(int xx=C-R;xx<=C+R;xx++){ if(xx<0||yy<0||xx>=W||yy>=W) continue; if(!occ[yy*W+xx]){
        double qx,qy; pos(xx,yy,&qx,&qy); double d2=qx*qx+qy*qy; if(d2<rin2) rin2=d2; double e2=(qx-cx)*(qx-cx)+(qy-cy)*(qy-cy); if(e2<ci2) ci2=e2; }
        else { double qx,qy; pos(xx,yy,&qx,&qy); double e2=(qx-cx)*(qx-cx)+(qy-cy)*(qy-cy); if(e2>co2) co2=e2; } }
      double rd=sqrt(k*area/M_PI);
      printf("%ld %.4f %.4f %.4f %.4f %ld %.6e %.4f %.4f %.4f\n",k,rd,sqrt(rout2)-rd,rd-sqrt(rin2),sqrt(rout2)-sqrt(rin2),steps,sumx2,cx,cy,sqrt(co2)-sqrt(ci2));
      fflush(stdout); next=(long)(next*1.25)+1;
    }
  }
  if(argc>5){ FILE*f=fopen(argv[5],"wb"); int R=(int)(sqrt(rout2)*1.3)+3; fwrite(&R,4,1,f);
    for(int yy=C-R;yy<=C+R;yy++)for(int xx=C-R;xx<=C+R;xx++){unsigned char v=occ[yy*W+xx]?(1+rot[yy*W+xx]):0; fwrite(&v,1,1,f);} fclose(f);}
  return 0;
}
