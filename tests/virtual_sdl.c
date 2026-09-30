#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
/* Test-only SDL virtual controllers. Never loaded by player launchers. */
static void *pads[2];
int SDL_Init(uint32_t flags) {
 setenv("SDL_JOYSTICK_DISABLE_UDEV","1",1);
 setenv("SDL_HIDAPI_JOYSTICK_DISABLE_UDEV","1",1);
 setenv("SDL_JOYSTICK_HIDAPI","0",1);
 setenv("SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS","1",1);
 int (*init)(uint32_t)=dlsym(RTLD_NEXT,"SDL_Init");
 int result=init(flags & ~(0x1000u|0x8000u));
 if(result!=0)return result;
 int (*count)(void)=dlsym(RTLD_NEXT,"SDL_NumJoysticks");
 const char*(*error)(void)=dlsym(RTLD_NEXT,"SDL_GetError");
 int (*attach)(int,int,int,int)=dlsym(RTLD_NEXT,"SDL_JoystickAttachVirtual");
 void *(*open)(int)=dlsym(RTLD_NEXT,"SDL_JoystickOpen");
 for(int i=0;i<2;i++)attach(1,6,15,0);
 void (*flush)(uint32_t,uint32_t)=dlsym(RTLD_NEXT,"SDL_FlushEvents");
 int (*push)(void*)=dlsym(RTLD_NEXT,"SDL_PushEvent");
 flush(0x605,0x605);
 for(int i=0;i<2;i++){
  pads[i]=open(i);
  union { uint8_t pad[56]; struct {uint32_t type,timestamp;int32_t which;} added; } event={0};
  event.added.type=0x605;event.added.which=i;push(&event);
  fprintf(stderr,"Virtual controller %d: count %d, opened %d\n",i,count(),pads[i]!=NULL);
 }
 return result;
}
int SDL_PollEvent(void *event) {
 int (*poll)(void *)=dlsym(RTLD_NEXT,"SDL_PollEvent");
 int (*button)(void*,int,uint8_t)=dlsym(RTLD_NEXT,"SDL_JoystickSetVirtualButton");
 void (*update)(void)=dlsym(RTLD_NEXT,"SDL_JoystickUpdate");
 const char *path=getenv("ETER_PAD_INPUT");unsigned int masks[2]={0,0};
 if(path){FILE*f=fopen(path,"r");if(f){int ok=fscanf(f,"%u %u",&masks[0],&masks[1]);(void)ok;fclose(f);}}
 for(int p=0;p<2;p++)if(pads[p])for(int b=0;b<15;b++)button(pads[p],b,(masks[p]>>b)&1);
 update();return poll(event);
}
