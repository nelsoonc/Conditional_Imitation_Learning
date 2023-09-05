#define throttlePin 2 // CH1 
#define steeringPin 3 // CH2
#define modePin 5 // CH7
#define commandPin 6 //CH11

int pulse[4];

void setup() {
  // put your setup code here, to run once:
  pinMode(throttlePin, INPUT);
  pinMode(steeringPin, INPUT);
  pinMode(modePin, INPUT);
  pinMode(commandPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  pulse[0] = pulseIn(throttlePin, HIGH);
  pulse[1] = pulseIn(steeringPin, HIGH);
  pulse[2] = pulseIn(modePin, HIGH);
  pulse[3] = pulseIn(commandPin, HIGH);
  Serial.println(String(pulse[0]) + "," + String(pulse[1]) +
  "," + String(pulse[2]) + "," + String(pulse[3]));
  delay(40);
}
