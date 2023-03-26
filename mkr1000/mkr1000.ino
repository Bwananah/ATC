const int interruptPin = 2; // Interrupt pin
volatile bool interruptFlag = false; // Interrupt flag

#define PROX_THRESHOLD  1500
#define MID_THRESHOLD  -20
const int trigPin1 = 6;
const int echoPin1 = 7;

const int trigPin2 = 8;
const int echoPin2 = 9;

const int trigPin3 = 10;
const int echoPin3 = 11;


volatile long duration1 = 0;
volatile long duration2 = 0;
volatile long duration3 = 0;
volatile boolean ready1 = false;
volatile boolean ready2 = false;
volatile boolean ready3 = false;

uint32_t sampleRate = 40; //sample rate in milliseconds, determines how often TC5_Handler is called


void setup() { 
  // Change this to Serial to print to the computer directly
  Serial.begin(115200);

  pinMode(trigPin1, OUTPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  pinMode(echoPin3, INPUT);
  
  Serial.println("Starting....");
  tcConfigure(sampleRate); //configure the timer to run at <sampleRate>Hertz
  tcStartCounter(); //starts the timer


}

void loop() {
  // If an object is within the threshold on any sensor
  if (duration1 > 0 && duration1 < PROX_THRESHOLD || duration2 > 0 && duration2 < PROX_THRESHOLD || duration3 > 0 && duration3 < PROX_THRESHOLD){  
  
    int left_edge = duration1 - duration2;
    int right_edge = duration3 - duration2;

    // First determine whether the object is more to the left or to the right
    if (left_edge < right_edge){
      // Then determine if it is more to the left or to the mid-left      
      if(left_edge > MID_THRESHOLD){
        Serial.println("mid");
      }else{
        Serial.println("left");
      }
    }else{
      if (right_edge > MID_THRESHOLD){
        Serial.println("mid");
      }else{
        Serial.println("right");
      }
    }
      //float distance3 = duration3 / 58.0;
  }else{
    Serial.println("nothing");
  }
}

  

//this function gets called by the interrupt at <sampleRate>Hertz
void TC5_Handler (void) {

  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

  duration1 = pulseIn(echoPin1, HIGH);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  duration2 = pulseIn(echoPin2, HIGH);

  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);

  duration3 = pulseIn(echoPin3, HIGH);
    
  // END OF YOUR CODE
  TC5->COUNT16.INTFLAG.bit.MC0 = 1; //Writing a 1 to INTFLAG.bit.MC0 clears the interrupt so that it will run again
}


/* 
 *  TIMER SPECIFIC FUNCTIONS FOLLOW
 *  you shouldn't change these unless you know what you're doing
 */

//Configures the TC to generate output events at the sample frequency.
//Configures the TC in Frequency Generation mode, with an event output once
//each time the audio sample frequency period expires.
 void tcConfigure(int sampleRate)
{
 // select the generic clock generator used as source to the generic clock multiplexer
 GCLK->CLKCTRL.reg = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID(GCM_TC4_TC5)) ;
 while (GCLK->STATUS.bit.SYNCBUSY);

 tcReset(); //reset TC5

 // Set Timer counter 5 Mode to 16 bits, it will become a 16bit counter ('mode1' in the datasheet)
 TC5->COUNT16.CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
 // Set TC5 waveform generation mode to 'match frequency'
 TC5->COUNT16.CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
 //set prescaler
 //the clock normally counts at the GCLK_TC frequency, but we can set it to divide that frequency to slow it down
 //you can use different prescaler divisons here like TC_CTRLA_PRESCALER_DIV1 to get a different range
 TC5->COUNT16.CTRLA.reg |= TC_CTRLA_PRESCALER_DIV1024 | TC_CTRLA_ENABLE; //it will divide GCLK_TC frequency by 1024
 //set the compare-capture register. 
 //The counter will count up to this value (it's a 16bit counter so we use uint16_t)
 //this is how we fine-tune the frequency, make it count to a lower or higher value
 //system clock should be 1MHz (8MHz/8) at Reset by default
 TC5->COUNT16.CC[0].reg = (uint16_t) (SystemCoreClock / sampleRate);
 while (tcIsSyncing());
 
 // Configure interrupt request
 NVIC_DisableIRQ(TC5_IRQn);
 NVIC_ClearPendingIRQ(TC5_IRQn);
 NVIC_SetPriority(TC5_IRQn, 0);
 NVIC_EnableIRQ(TC5_IRQn);

 // Enable the TC5 interrupt request
 TC5->COUNT16.INTENSET.bit.MC0 = 1;
 while (tcIsSyncing()); //wait until TC5 is done syncing 
} 

//Function that is used to check if TC5 is done syncing
//returns true when it is done syncing
bool tcIsSyncing()
{
  return TC5->COUNT16.STATUS.reg & TC_STATUS_SYNCBUSY;
}

//This function enables TC5 and waits for it to be ready
void tcStartCounter()
{
  TC5->COUNT16.CTRLA.reg |= TC_CTRLA_ENABLE; //set the CTRLA register
  while (tcIsSyncing()); //wait until snyc'd
}

//Reset TC5 
void tcReset()
{
  TC5->COUNT16.CTRLA.reg = TC_CTRLA_SWRST;
  while (tcIsSyncing());
  while (TC5->COUNT16.CTRLA.bit.SWRST);
}

//disable TC5
void tcDisable()
{
  TC5->COUNT16.CTRLA.reg &= ~TC_CTRLA_ENABLE;
  while (tcIsSyncing());
}