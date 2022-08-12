
/*
    Teensy4.1 Glide program
    Read R/C servo wireless receiver 8 channels and read pulse length in microseconds
    Uses interrupts on signsl changes
    Using RadioLink xmt/rcv  'B' pair

    Pulse haptic actuators

    Read torque sensor for user steering
*/

//#include <Servo.h>                           // Include servo library
#include "HX711.h"

/*
//These 8 are signals from the remote controlled R/C receiver
#define Ch1 1  //RC servo receiver outputpin #1 to Teensy input for steering from remote
#define Ch2 2 //futu
#define Ch3 3 //RC servo receiver output pin#3 it Teensy input for braking from remote
#define Ch4 4
#define Ch5 5
#define Ch6 6
#define Ch7 7
//#define Ch8 8   //no chl8
*/

#define CHA_R 38  //Wheel encoder quadrature outputs
#define CHB_R 39
#define CHA_L 40
#define CHB_L 41

/*
Servo SteerServoOut;  // Declare steering servo output signal
Servo BrakeServoOut;  // Declare brake servo output signal

Servo ServoOut2;    // Declare servo2 signal for later use
Servo ServoOut4;    // Declare servo4 signal
*/

HX711 TorqueSensor;

volatile byte val = 0; //

//wheel encoder variables
volatile int master_count_L = 0; // universal wheel rev count for left wheel
volatile int master_count_R = 0; // universal rev count for right wheel
volatile byte INTFLAG_L = 0; // interrupt status flag for left encoder
volatile byte INTFLAG_R = 0; // interrupt status flag for right encoder
volatile int Lincr, Rincr;  // left and right wheel enc increments

int InByte = 0; //serial input char
int SerInFlag = 0;  //Serial Input flaag

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 17;
const int LOADCELL_SCK_PIN = 16;

/*
  int SteerPeriod = 1500;  // Steering servo pulse period to Steering Servo
  int SteerOffset = 84; // offset to steer straight
  int BrakePeriod = 2000;
  int BrakeOffset = -600;

  int Ch1StartTime = 0; //value of internal microsecond clock when ch1 goes high
  int Ch1Period = 0;  // total ch1 period in microseconds
  int Ch2StartTime = 0;
  int Ch2Period = 0;
  int Ch3StartTime = 0;
  int Ch3Period = 0;
  int Ch4StartTime = 0;
  int Ch4Period = 0;
  int Ch5StartTime = 0; //microsecond clock when ch5 goes high
  int Ch5Period = 0;  // total ch5 period in microseconds
  int Ch6StartTime = 0;
  int Ch6Period = 0;
  int Ch7StartTime = 0;
  int Ch7Period = 0;
  int Ch8StartTime = 0;
  //int Ch8Period = 0;
 
  float SteerPeriodFlt = 1000;  //Steering signal filtered
  float Ch1PeriodFlt = 1000; //Rcvr ch1period (steering) filtered)
*/

int Torque = 0; //Torque from torque sensor on handle.  Via I2C comm
float TorqueFlt = 0; //handle torque avg filtered value to reduce drift
int i = 0;
int j = 0;
int(pin);

int Actuator[7] = {0, 9, 10, 11, 12, 24, 25}; //Glide handle actuators

void setup() {
  
  //Wheel enc pins init
  pinMode(CHA_L, INPUT_PULLUP); //left wheel encoder A with an internal pulluip resistor
  pinMode(CHB_L, INPUT_PULLUP);
  pinMode(CHA_R, INPUT_PULLUP); //right  wheel encoder A
  pinMode(CHB_R, INPUT_PULLUP);

  //wheel enc ISR
  attachInterrupt(CHA_L, Flag_L, RISING); //format OK for Teensy4.1
  attachInterrupt(CHA_R, Flag_R, RISING);

  pinMode(0, OUTPUT); //diag output pin
  //pinMode(9, OUTPUT);   //   "

  // initialize the Haptic output digital pins as an outputs for haptic actuators.
  for (i = 1; i < 7; i++) //make all actuator pins output
  {
    pin = Actuator[i];
    pinMode(pin, OUTPUT);
    digitalWrite(Actuator[i], LOW);
  }

  for ( i = 0; i < 10; i++) //turn off actuators asap
  {
    for (j = 1; j < 7 ; j++)
    {
      digitalWrite(Actuator[j], LOW);
    }
  }

  pinMode(0, OUTPUT);   //diagnistic output pin

  /*
    Ch1PeriodFlt = 1500;  //seed the filter value to idle position
    SteerServoOut.attach(22);  // Attach servo steering signal to pin 22
    //  ServoOut2.attach(15);  //future
    BrakeServoOut.attach(23);  // Attach braking signal to pin 23
    //  ServoOut4.attach(17); //future

    SteerServoOut.writeMicroseconds(1580);      // set the idle period for steering straight, pin 14
    //  ServoOut2.writeMicroseconds(2000);      // 1.5 ms idle sig, pin 15 for future
    BrakeServoOut.writeMicroseconds(2000);      // 2 ms idle, no-brake sig, pin 16
    //  ServoOut4.writeMicroseconds(1500);    // 1.5 ms idle sig, pin 16, for future

    pinMode(Ch1, INPUT);    //make servo Ch1 pin an input to read chl1 of R/C radio rcvr
    pinMode(Ch2, INPUT);
    pinMode(Ch3, INPUT);
    pinMode(Ch4, INPUT);
    pinMode(Ch5, INPUT);
    pinMode(Ch6, INPUT);
    pinMode(Ch7, INPUT);
    //pinMode(Ch8, INPUT);  //not connected
  */

  TorqueSensor.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN); //torque sensor (I2C comm)

  Serial.begin(230400); //use high speed serial for diag printout though Teensy seems to
  // ignore and prints at highest speed possible
  Serial.print("GlideHero2 program");
  
  //    assign ISRs to R/C receiver servo output signals
  /*
    attachInterrupt(Ch1, Ch1Change, CHANGE);  //Right X-joystick, steering. MoveLeft = minimum period
    //attachInterrupt(Ch2, Ch2Change, CHANGE);  //Right Y-joystick. Up = minimum
    attachInterrupt(Ch3, Ch3Change, CHANGE);  //Left Y-joustick, braking.  Down = minimum period
    // attachInterrupt(Ch4, Ch4Change, CHANGE);  //Left Y-joystick. Left = Minimum
    //  attachInterrupt(Ch5, Ch5Change, CHANGE);  //Right 3pos button. Up=2ms, mid=1.5ms, down=1ms
    attachInterrupt(Ch6, Ch6Change, CHANGE);  //Right trigger. NoTrig=1ms, Trig=2ms
    //  attachInterrupt(Ch7, Ch7Change, CHANGE);  //Left 3pos button. Up=2ms, mid=1.5ms, down=1ms
    // attachInterrupt(Ch8, Ch8Change, CHANGE);  //Left pot knob. Left = 1ms, Right = 2ms
  */

  /*
    //Do a one time demo of handle haptic acutuators.
    // Pulse all actuators on and off fast, repeat 5 times
    for ( i = 0; i < 5; i++)
    {
      for (j = 1; j < 7 ; j++)    //turn them all on
      {
        digitalWrite(Actuator[j], HIGH);  //turn on
      }
      delay(70);

      for (j = 1; j < 7 ; j++)
      {
        digitalWrite(Actuator[j], LOW);   //turn off
      }
      delay(70);
    }
    delay(2000);  //wait 2 second

    // Pulse the left actuator, repeat 5 times
    for ( i = 0; i < 5; i++)
    {
      //for (j = 1; j < 3 ; j++)
      j = 1;
      {
        digitalWrite(Actuator[j], HIGH);
      }
      delay(70);

      //for (j = 1; j < 3 ; j++)
      j = 1;
      {
        digitalWrite(Actuator[j], LOW);
      }
      delay(70);
    }
    delay(2000);

    // Pulse the right actuator, repeat 5 times
    for ( i = 0; i < 5; i++)
    {
      j = 6;
      {
        digitalWrite(Actuator[j], HIGH);
      }
      delay(70);
      j = 6;
      {
        digitalWrite(Actuator[j], LOW);
      }
      delay(70);
    }
    delay(2000);

    // L->R sweep, one at a time
    for ( i = 0; i < 4; i++)
    {
      for (j = 1; j < 7 ; j++)
      {
        digitalWrite(Actuator[j], HIGH);
        delay(100);
        digitalWrite(Actuator[j], LOW);
      }
      delay(300);
    }
    delay(2000);

    // R->L sweep, one at a time
    for ( i = 0; i < 6; i++)
    {
      for (j = 1; j < 7 ; j++)
      {
        digitalWrite(Actuator[7 - j], HIGH);
        delay(100);
        digitalWrite(Actuator[7 - j], LOW);
      }
      delay(300);
    }
    delay(2000);
  */
  
    } //end Setup

  void loop() {

    digitalWrite(0, HIGH); //diagnostic pin. Pulse every lo
    //Serial.print("--------------------------------------------------");
   // digitalWrite(0, LOW);

    if (TorqueSensor.is_ready()) {  //read strain guage torque sensor thru I2C comm
      long Torque = TorqueSensor.read(); //I2C read torque sensor
      Torque = Torque + 118000.0; //offset
      Torque = Torque >> 8; //scale down
      
      Serial.print(Torque);
      Serial.print(" ");
      Serial.print(master_count_L);
      Serial.print(" ");
      Serial.println(master_count_R);
      master_count_L = 0;  //reset 
      master_count_R = 0;
      
      //TorqueFlt = ((TorqueFlt)  + float(Torque)) / 2.0; // avg value, filtered by 1:1
    }

    /*
      //TorqueFlt = ((TorqueFlt) * 999.0 + float(Torque)) / 1000.0; // avg value, filtered by 255:1
      //Ch1PeriodFlt = ((Ch1PeriodFlt * 63.0) + float(Ch1Period)) / 64.0;

      SteerPeriod = int(Ch1PeriodFlt) + SteerOffset + TorqueFlt;   // - int(TorqueFlt);  //overall steering
      //SteerPeriod = int(Ch1PeriodFlt);

      if (SteerPeriod > 2000) {   //limit steering to 1ms < steering-period < 2ms
        SteerPeriod = 2000;
      }
      if (SteerPeriod < 1000) {
        SteerPeriod = 1000;
      }
      SteerServoOut.writeMicroseconds(SteerPeriod);
      BrakeServoOut.writeMicroseconds(BrakePeriod);
    */

    digitalWrite(0, LOW); //diagnostic time

    if (INTFLAG_L)   {    //Check to see if interrupt from left encoder
      INTFLAG_L = 0;  //clr interrupt flag
      //master_count_L = master_count_L % 600;  // output only per rev count
      //Serial.print("L");
      //Serial.print(master_count_R);
      
      //Serial.print("0");
      //Serial.print(",");
      //Serial.println(Lincr);
      
      //Serial.println(master_count_L);
      //Serial.print("\t");
      //Serial.println(master_count_R);
    }

    if (INTFLAG_R)   {    //if interrupt from right encoder
      INTFLAG_R = 0; // clear flag
      //master_count_R = master_count_R % 600;  // output only per rev count
      //Serial.print(master_count_R);
      
      //Serial.print(Rincr);  //changed L <-> R due to brake prob Works w Batt to rear
      //Serial.print(",");
      //Serial.println("0");

      //Serial.println(master_count_L);
    }

    /*
      //Serial.print(Ch1Period);
      //Serial.print("\t");
      //Serial.print(Ch1PeriodFlt);
      //Serial.print(SteerPeriod);
      //Serial.print("\t");
      //Serial.print(Ch2Period);
      //Serial.print("\t");
      //Serial.print(Ch3Period);
      //Serial.print("\t");
      //Serial.print(Torque - int(TorqueFlt));
      //Serial.print("\t");

      //Serial.print(Ch4Period);
      //Serial.print("\t");
      //Serial.print(Ch5Period);
      //Serial.print("\t");
      //Serial.print(Ch6Period);
      //Serial.print("\t");
      //Serial.print(Ch7Period);
      //Serial.print("\t");
      //  Serial.print(Ch8Period);
      // Serial.print("\t");
      //Serial.println("-");
    */
  } //end Loop

void Flag_L() {
  INTFLAG_L = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_L) && !digitalRead(CHB_L)) {
    master_count_L-- ;
    Lincr = -1;
  }
  else
  {
    // subtract 1 from count for CCW
    //if (digitalRead(CHA_L) && digitalRead(CHB_L)) {
    master_count_L++ ;
    Lincr = 1;
  }
}

void Flag_R() {
  INTFLAG_R = 1;
  // add 1 to count for CW
  if (digitalRead(CHA_R) && !digitalRead(CHB_R)) {
    master_count_R++ ;
    Rincr = 1;
  }

  // else subtract 1 from count for CCW
  if (digitalRead(CHA_R) && digitalRead(CHB_R)) {
    master_count_R--;
    Rincr = -1;
  }
}
  //______________________________________________________________________________________

  /*
    void Ch1Change() {  //detected a pulse change in R/C receiver, Ch1, steering
    val = digitalRead(Ch1);
    if (val == 1) {
      Ch1StartTime = micros() ;
    }
    else {
      Ch1Period = micros() - Ch1StartTime;
    }
    Ch1PeriodFlt = ((Ch1PeriodFlt * 7.0) + float(Ch1Period)) / 8.0; //low pass
    TorqueFlt = ((TorqueFlt) * 3.0 + float(Torque)) / 4.0; // avg value, filtered by 255:1
    }

    void Ch2Change() {  //detected a change on edge of rcvr Ch2
    val = digitalRead(Ch2);
    if (val == 1) {
      Ch2StartTime = micros() ;
    }
    else {
      Ch2Period = micros() - Ch2StartTime;
    }
    }

    void Ch3Change() {  //detected a change R/C receiver on edge of Ch3, braking
    val = digitalRead(Ch3);
    if (val == 1) {
      Ch3StartTime = micros() ;
    }
    else {
      Ch3Period = micros() - Ch3StartTime;
    }
    BrakePeriod = 3000 - Ch3Period + BrakeOffset;
    //BrakeServoOut.writeMicroseconds(BrakePeriod);
    }

    void Ch4Change() {  //detected a change on edge on Ch4
    val = digitalRead(Ch4);
    if (val == 1) {
      Ch4StartTime = micros() ;
    }
    else {
      Ch4Period = micros() - Ch4StartTime;
    }
    }

    void Ch5Change() {  //detected a change in Ch5
    val = digitalRead(Ch5);
    if (val == 1) {
      Ch5StartTime = micros() ;
    }
    else {
      Ch5Period = micros() - Ch5StartTime;
    }
    }

    void Ch6Change() {  //detected a change on edge on Ch6
    val = digitalRead(Ch6);
    if (val == 1) {
      Ch6StartTime = micros() ;
    }
    else {
      Ch6Period = micros() - Ch6StartTime;
    }

    if (Ch6Period > 1500) { //see if rt trigger pressed
      for (j = 1; j < 7 ; j++)    //turn them all on if right trigger pushed
      {
        digitalWrite(Actuator[j], HIGH);  //turn on
      }
    }
      else
      { for (j = 1; j < 7 ; j++)    //turn them all on
        {
          digitalWrite(Actuator[j], LOW);  //turn off
        }

      }
    }

    void Ch7Change() {  //detected a change on edge on Ch7
      val = digitalRead(Ch7);
      if (val == 1) {
        Ch7StartTime = micros() ;
      }
      else {
        Ch7Period = micros() - Ch7StartTime;

      }
    }
  */

  /*  No chl 8 presently
    void Ch8Change() {  //detected a change on edge on Ch8
    val = digitalRead(Ch8);
    if (val == 1) {
      Ch8StartTime = micros() ;
    }
    else {
      Ch8Period = micros() - Ch8StartTime;
      LastServoFlag = 1;  //the last RC servo signal (H to L) transition
    }
    }
  */