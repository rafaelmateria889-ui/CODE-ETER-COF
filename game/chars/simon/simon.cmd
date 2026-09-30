[Remap]
x = x
a = a
y = y
b = b
[Defaults]
command.time = 22
command.buffer.time = 4

[Command]
name = "super"
command = ~D, DF, F, D, DF, F, x+y
time = 32

[Command]
name = "qcf"
command = ~D, DF, F, x
time = 24

[Command]
name = "qcb"
command = ~D, DB, B, x
time = 24

[Command]
name = "dp"
command = F, D, DF, x
time = 24

[Command]
name = "grab"
command = x+a
time = 1

[Command]
name = "dash"
command = F,F
time = 12

[Command]
name = "backdash"
command = B,B
time = 12

[Command]
name = "step"
command = ~D, DB, B, a
time = 24

[Command]
name = "throwsp"
command = F,D,DF,a
time = 24

[Command]
name = "servoH"
command = ~D, DB, B, b
time = 24

[Command]
name = "qcfH"
command = ~D, DF, F, y
time = 24

[Command]
name = "qcbH"
command = ~D, DB, B, y
time = 24

[Command]
name = "dpH"
command = F, D, DF, y
time = 24

[Command]
name = "throwspH"
command = F, D, DF, b
time = 24

[Command]
name = "x"
command = x
time = 1

[Command]
name = "a"
command = a
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "c"
command = c
time = 1

[Command]
name = "z"
command = z
time = 1

[Command]
name = "holdfwd"
command = /$F
time = 1
buffer.time = 1

[Command]
name = "holdback"
command = /$B
time = 1
buffer.time = 1

[Command]
name = "holdup"
command = /$U
time = 1
buffer.time = 1

[Command]
name = "holddown"
command = /$D
time = 1
buffer.time = 1

[Statedef -1]

[State 0, super]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "super"
triggerall = Power >= 1000
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 3000

[State 0, dp]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "dp"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1200

[State 0, qcf]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "qcf"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1100

[State 0, qcb]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "qcb"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1000

[State 0, step]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "step"
triggerall = NumHelper(1450) = 0
triggerall = var(5) = 0
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1400

[State 0, throwsp]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "throwsp"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1300

[State 0, servoH]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "servoH"
triggerall = NumHelper(1450) = 0
triggerall = var(5) = 0
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1401

[State 0, dpH]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "dpH"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1201

[State 0, qcfH]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "qcfH"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1101

[State 0, qcbH]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "qcbH"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1001

[State 0, throwspH]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = StateType != A
triggerall = command = "throwspH"
trigger1 = Ctrl
trigger2 = MoveContact && (StateNo = 200 || StateNo = 210 || StateNo = 220 || StateNo = 400 || StateNo = 410 || StateNo = 420)
value = 1301

[State 0, c]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "c"
triggerall = StateType != A
trigger1 = Ctrl
value = 1000

[State 0, z]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "z"
triggerall = StateType != A
trigger1 = Ctrl
value = 1100

[State 0, grab]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "grab"
triggerall = StateType != A
trigger1 = Ctrl
value = 800

[State 0, dash]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "dash"
triggerall = StateType != A
trigger1 = Ctrl
value = 100

[State 0, backdash]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "backdash"
triggerall = StateType != A
trigger1 = Ctrl
value = 105

[State 0, Normal x]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "x"
trigger1 = Ctrl
value = ifelse(StateType = A,600,ifelse(command = "holddown",400,200))

[State 0, Normal a]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "a"
trigger1 = Ctrl
value = ifelse(StateType = A,610,ifelse(command = "holddown",410,210))

[State 0, Normal y]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "y"
trigger1 = Ctrl
value = ifelse(StateType = A,620,ifelse(command = "holddown",420,220))

[State 0, Normal b]
type = ChangeState
triggerall = AILevel = 0
triggerall = RoundState = 2
triggerall = command = "b"
trigger1 = Ctrl
value = ifelse(StateType = A,630,ifelse(command = "holddown",430,230))

[State 0, Chain y]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "y"
triggerall = MoveContact
trigger1 = StateNo = 200 || StateNo = 210
value = 220

[State 0, Chain b]
type = ChangeState
triggerall = AILevel = 0
triggerall = command = "b"
triggerall = MoveContact
trigger1 = StateNo = 200 || StateNo = 210
value = 230
