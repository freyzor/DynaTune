/* 
  ArbotiX Test Program for use with PyPose 0015
  Copyright (c) 2008-2011 Michael E. Ferguson.  All right reserved.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/
 
#include <ax12.h>

#define DYNATUNE_BAUD 1000000

#define ARB_TEST        25

int mode = 0;                   // where we are in the frame

unsigned char id = 0;           // id of this frame
unsigned char length = 0;       // length of this frame
unsigned char ins = 0;          // instruction of this frame

unsigned char params[143];      // parameters (match RX-64 buffer size)
unsigned char index = 0;        // index in param buffer

int checksum;                   // checksum


void setup(){
    Serial.begin(38400); 
    ax12Init(DYNATUNE_BAUD); 
    pinMode(0,OUTPUT);          // status LED
}

/* 
 * packet: ff ff id length ins params checksum
 *   same as ax-12 table, except, we define new instructions for Arbotix
 *
 * ID = 253 for these special commands!
 * TEST
 */
#define STATE_START                 0
#define STATE_READ_SERVO_ID         2
#define STATE_READ_LENGTH           3
#define STATE_READ_INSTRUCTION      4
#define STATE_READ_DATA_INPUT       5

void sendError(int id, unsigned char errorCode){
    // return a packet: FF FF id Len Err params=None check
    Serial.write(0xff);
    Serial.write(0xff);
    Serial.write(id);
    Serial.write(2);
    Serial.write(errorCode);
    Serial.write(255-((2+errorCode+id)%256));
}

void loop(){
    int i;
    
    // process messages
    while(Serial.available() > 0){
        // We need to 0xFF at start of packet
        if(mode == STATE_START){         // start of new packet
            if(Serial.read() == 0xff){
                mode = STATE_READ_SERVO_ID;
                digitalWrite(0,HIGH-digitalRead(0));
            }

        }else if(mode == STATE_READ_SERVO_ID){   // next byte is index of servo
            id = Serial.read();    
            if(id != 0xff)
                mode = STATE_READ_LENGTH;

        }else if(mode == STATE_READ_LENGTH){   // next byte is length
            length = Serial.read();
            checksum = id + length;
            mode = STATE_READ_INSTRUCTION;

        }else if(mode == STATE_READ_INSTRUCTION){   // next byte is instruction
            ins = Serial.read();
            checksum += ins;
            index = 0;
            mode = STATE_READ_DATA_INPUT;

        }else if(mode == STATE_READ_DATA_INPUT){   // read data in 
            params[index] = Serial.read();
            checksum += (int) params[index];
            index++;
            if(index + 1 == length){  // we've read params & checksum
                mode = STATE_START;

                if((checksum%256) != 255){
                    sendError(id, 64);
                }else{
                    if(id == 253){
                        sendError(id, 0);

                        // special ArbotiX instructions
                        if(ins == ARB_TEST){
                            int i;
                            // Test Ax-12
                            for(i=452;i<552;i+=20){
                                SetPosition(1,i);
                                delay(200);
                            }
                        }   
                    }else{
                        int i;
                        // pass thru
                       if(ins == AX_READ_DATA){
                            int i;
                            ax12GetRegister(id, params[0], params[1]);
                            // return a packet: FF FF id Len Err params check
                            if(ax_rx_buffer[3] > 0){
                            for(i=0;i<ax_rx_buffer[3]+4;i++)
                                Serial.write(ax_rx_buffer[i]);
                            }
                            ax_rx_buffer[3] = 0;
                        }else if(ins == AX_WRITE_DATA){
                            if(length == 4){
                                ax12SetRegister(id, params[0], params[1]);
                            }else{
                                int x = params[1] + (params[2]<<8);
                                ax12SetRegister2(id, params[0], x);
                            }
                            sendError(id, 0);
                        }
                    }
                }
            }
        }
    }
}

