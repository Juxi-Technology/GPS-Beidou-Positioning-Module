/**********************************************************											
接线说明：
STM32					GPS
VCC		------>	VCC
GND		------>	GND
PA10  <------	TXD


STM32					USB-TTL模块
GND		------>	GND
PA9		------>	RXD
***********************************************************/

#include "stm32f10x.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "stdlib.h"

//声明
void errorLog(int num);
void parseGpsBuffer(void);
void printGpsBuffer(void);

int main(void)
{	
	delay_init();
	
	NVIC_Configuration(); 	 //设置NVIC中断分组2:2位抢占优先级，2位响应优先级
	uart_init(9600);	 //串口初始化为9600
	Init_LEDpin();
	LED1 = 1;
	
	clrStruct();
	
	printf("Welcome to use!\r\n");
	while(1)
	{
		parseGpsBuffer();
		printGpsBuffer();
	}
}

void errorLog(int num)
{
	
	while (1)
	{
	  	printf("ERROR%d\r\n",num);
	}
}

void parseGpsBuffer()
{
	char *subString;
	char *subStringNext;
	char i = 0;
	if (Save_Data.isGetData)
	{
		Save_Data.isGetData = false;
		printf("**************\r\n");
		printf(Save_Data.GPS_Buffer);

		
		for (i = 0 ; i <= 6 ; i++)
		{
			if (i == 0)
			{
				if ((subString = strstr(Save_Data.GPS_Buffer, ",")) == NULL)
					errorLog(1);	//解析错误
			}
			else
			{
				subString++;
				if ((subStringNext = strstr(subString, ",")) != NULL)
				{
					char usefullBuffer[2]; 
					switch(i)
					{
						case 1:memcpy(Save_Data.UTCTime, subString, subStringNext - subString);break;	//获取UTC时间
						case 2:memcpy(usefullBuffer, subString, subStringNext - subString);break;	//获取UTC时间
						case 3:memcpy(Save_Data.latitude, subString, subStringNext - subString);break;	//获取纬度信息
						case 4:memcpy(Save_Data.N_S, subString, subStringNext - subString);break;	//获取N/S
						case 5:memcpy(Save_Data.longitude, subString, subStringNext - subString);break;	//获取经度信息
						case 6:memcpy(Save_Data.E_W, subString, subStringNext - subString);break;	//获取E/W

						default:break;
					}

					subString = subStringNext;
					Save_Data.isParseData = true;
					if(usefullBuffer[0] == 'A')
						Save_Data.isUsefull = true;
					else if(usefullBuffer[0] == 'V')
						Save_Data.isUsefull = false;

				}
				else
				{
					errorLog(2);	//解析错误
				}
			}
		}
	}
}

// GPS数据转化单位为度。
double Convert_to_degrees(char* data)
{
	double temp_data = atof(data);
	int degree = (int)(temp_data / 100);
	double f_degree = (temp_data / 100.0 - degree)*100/60.0;
	double result = degree + f_degree;
	return result;
}


void printGpsBuffer()
{
	double f_latitude = 0.0;
	double f_longitude = 0.0;
	
	if (Save_Data.isParseData)
	{
		Save_Data.isParseData = false;
		
		printf("Save_Data.UTCTime = ");
		printf(Save_Data.UTCTime);
		printf("\r\n");

		if(Save_Data.isUsefull)
		{
			Save_Data.isUsefull = false;
			printf("Save_Data.latitude = ");
			// printf(Save_Data.latitude);
			// printf("--");
			f_latitude = Convert_to_degrees(Save_Data.latitude);
			printf("%lf%s", f_latitude, Save_Data.N_S);
			printf("\r\n");

			printf("Save_Data.N_S = ");
			printf(Save_Data.N_S);
			printf("\r\n");

			printf("Save_Data.longitude = ");
			// printf(Save_Data.longitude);
			// printf("--");
			f_longitude = Convert_to_degrees(Save_Data.longitude);
			printf("%lf%s", f_longitude, Save_Data.E_W);
			printf("\r\n");

			printf("Save_Data.E_W = ");
			printf(Save_Data.E_W);
			printf("\r\n");
		}
		else
		{
			printf("GPS DATA is not usefull!\r\n");
		}
		
	}
}
