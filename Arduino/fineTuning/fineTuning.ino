#define throttlePin 2 // CH1 
#define steeringPin 3 // CH2

int pulse[2];

void setup() {
  // put your setup code here, to run once:
  pinMode(throttlePin, INPUT);
  pinMode(steeringPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  pulse[0] = pulseIn(throttlePin, HIGH);
  pulse[1] = pulseIn(steeringPin, HIGH);

  Serial.println(to_bit(pulse[1]));
  delay(40);
}

int to_bit(int pulse) {
  return int(pulse * (4095.0/20000.0));
}
