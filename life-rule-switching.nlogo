patches-own [
  next-pcolor ;; the next state is calculated using current pcolor
]

globals [
  living1k
]

;; clear the board and create some life
to setup
  ;; standard setup
  clear-all
  reset-ticks

  ;; data collected during the game
  set living1k []

  ;; make the world with custom size
  resize-world 0 (world-size - 1) 0 (world-size - 1)

  ;; heuristic scaling of the patch size
  set-patch-size floor ( 50 / (sqrt world-size) )

  ;; use next-pcolor to initialize pcolor
  ask patches [
    ifelse random 100 < init-life [
      set next-pcolor black
    ][
      set next-pcolor white
    ]
    set pcolor next-pcolor
  ]
end

;;
;; main function
;;
to go

  ifelse synchronous [
    ask patches [
      simulate-life
    ]
    ask patches [
      update-state
    ]
  ][
    ask patches [
      simulate-life
      update-state
    ]
  ]

  update-living1k
  tick
end

;;
;; calculate the updating rule
;;
to  simulate-life
  ifelse deterministic [ ;; deterministic rule switching
    ifelse ticks mod deterministic-period = 0 [
      update-rule-modified
    ][ ;; ticks mod deterministic-period \= 0
      update-rule-std
    ]
  ][ ;; random rule switching
    ifelse random-float 1 > rule-switch-prob [
      update-rule-std
    ][
      update-rule-modified
    ]
  ]
end

;;
;; standard update rule for the Game of Life
;;
to update-rule-std
  let x (count neighbors with [ pcolor = black] )

  ifelse pcolor = black [
    ifelse x < 2 or x >= 4 [ ;; x>=4 (weak inequality) - standard rule
      set next-pcolor white ;; ie. die
    ][
      set next-pcolor black ;; ie. stay alive
    ]
  ][ ;; pcolor = white
    if x >= 3 and x < 4 [ ;; modified rule if second-threshold != 4
          set next-pcolor black ;; ie. birth
    ]
  ]
end

;;
;; update rule with the altered treshold for the overpopulation
;;
to update-rule-modified
  let x (count neighbors with [ pcolor = black] )

  ifelse pcolor = black [
    ifelse x < 2 or x >= second-threshold [ ;; modified rule if second-threshold != 4
      set next-pcolor white ;; ie. die
    ][
      set next-pcolor black ;; ie. stay alive
    ]
  ][ ;; pcolor = white
    if x >= 3 and x < second-threshold [ ;; modified rule if second-threshold != 4
          set next-pcolor black ;; ie. birth
    ]
  ]
end

;;
;; update the state
;;
to update-state
  set pcolor next-pcolor
end

;;
;; reporters
;;

;;
;; percentage of living cells
;;
to-report %living
  report 100 * ( count patches with [ pcolor = black] ) / ( count patches )
end

;;
;; fraction of living cells
;;
to-report living-fraction
  report ( count patches with [ pcolor = black] ) / ( count patches )
end

;;
;;
;;
to update-living1k
  ;; add current vale of cooperators-fraction to the list cooperators1k
  set living1k fput living-fraction living1k
end

;;
;;
;;
to-report mean-living1k
  ifelse ticks >= 1000 [
    report mean ( sublist living1k 0 1000 )
  ][
    report -1
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
210
10
602
403
-1
-1
6.0
1
10
1
1
1
0
1
1
1
0
63
0
63
1
1
1
ticks
30.0

BUTTON
21
304
191
337
Setup world
setup
NIL
1
T
OBSERVER
NIL
S
NIL
NIL
1

SLIDER
17
51
188
84
init-life
init-life
0
100
50.0
1
1
NIL
HORIZONTAL

SLIDER
18
12
190
45
world-size
world-size
10
300
64.0
1
1
NIL
HORIZONTAL

BUTTON
20
345
99
378
Play life
go
NIL
1
T
OBSERVER
NIL
P
NIL
NIL
1

BUTTON
105
344
192
377
Loop
go
T
1
T
OBSERVER
NIL
F
NIL
NIL
1

MONITOR
624
271
725
316
% of living cells
%living
4
1
11

SWITCH
19
95
190
128
synchronous
synchronous
1
1
-1000

SLIDER
17
218
189
251
rule-switch-prob
rule-switch-prob
0
1
0.5
0.01
1
NIL
HORIZONTAL

BUTTON
18
385
188
418
Play 50 times
repeat 50 [go]
NIL
1
T
OBSERVER
NIL
T
NIL
NIL
1

SLIDER
18
260
190
293
second-threshold
second-threshold
2
9
8.0
1
1
NIL
HORIZONTAL

SWITCH
18
138
189
171
deterministic
deterministic
0
1
-1000

PLOT
625
14
925
238
fraction of living cells
step
fraction of living cells
0.0
60.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -10899396 true "" "plot living-fraction"

SLIDER
18
179
188
212
deterministic-period
deterministic-period
1
100
2.0
1
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

This model implements a version of Game of Life cellular 2D automaton extended with the ability to alter the rules utilized by the cell during the evolution. Simple versions of random and deterministic mechanisms of rules selection are implemented. In both case, at each step, the cell can be updated according to one of the rules - the standard one and the alternative one. The standard rule is identical to the rule for dying due to overpopulation (Any live cell with four or more live neighbors dies, because of the  overpopulation). The alternative rule for threshold _r_ is: Any live cell with _r_ of more live neighbors dies, because of the  overpopulation.

Additionally, one can switch between synchronous and asynchronous state updating policy. In the synchronous update policy, corresponding to the standard version of GoL, the state of the lattice is updated globally at the end of each simulation step. In the asynchronous policy, the state of each agent is calculated and updated immediately. Thus, each simulation steps consists of the calculation of next state of the cell, and the update of the cell state. The order of cells is chosen randomly

## HOW IT WORKS

Game of Live is a 2D cellular automaton. Black color marks living cells, white cells are dead. In the basic version of the game - synchronous stat updating and single evolution rule - cells can become live or dead according to threshold on the number of living cells in their neighborhood.

The following parameters of the model are available through the controls:

* _world-size_ - size of the lattice used to run the simulation;
* _init-life_ - percentage of living cells at the beginning of the simulation;
* _synchronous_ - toggle between synchronous and asynchronous updating policy;
* _deterministic_ - toggle between deterministic and random rule selection mechanism;
* _deterministic-period_ - the number of iteration between the utilization of the alternative rule in the deterministic rule switching mechanism;
* _rule-switch-prob_ - set the probability of utilizing an alternative rule in the random rule switching mechanism;
* _second-threshold_ - threshold used in the second (alternative) rule used in the game;

## HOW TO USE IT

After setting the required parameters, use _Setup world_ button to initialize the simulation. To run the model ones, use _Play life_ button. _Loop_ button runs the game in a loop, and _Play 50 times_ runs 50 simulation cycles.

## THINGS TO NOTICE

The formation of patterns and the stability of the evolution depends on the selection of parameters. 

Some popular formation could occur in the case of synchronous or asynchronous updating. It is possible to switch between synchronous and asynchronous updating during the game to observe the changes in the behavior.

Similarly, in the case of random mechanism for selecting rules, it is possible to change the probability of switching between the base rule and the alternative rule.

## THINGS TO TRY

The most important element to try is to modify the threshold for dying due to the underpopulation.

## EXTENDING THE MODEL

Currently, all patches are updated during each step. To explore the transition between synchronous and asynchronous policy, only a fraction of the cell should update its state synchronously. This could be achieved by introducing a new parameter defining the probability of synchronous updating.

## RELATED MODELS
Conway’s Game of Life, http://www.modelingcommons.org/browse/one_model/6948

## CREDITS AND REFERENCES

Conway's Game of Life, https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
Asynchronous cellular automaton, https://en.wikipedia.org/wiki/Asynchronous_cellular_automaton

A model of the Game of Life with asynchronous updating was introduced in 
H.J. Blok, B. Bergersen, "Synchronous versus asynchronous updating in the “game of Life”", Phys. Rev. E 59, 3876 (1999), https://doi.org/10.1103/PhysRevE.59.3876

1D cellular automata with random updating due to the noise were studied in 

Louis, P.-Y., &#38; Nardi, F. R. (Eds.). (2018). Probabilistic Cellular Automata (Vol. 27). Springer International Publishing. https://doi.org/10.1007/978-3-319-65558-1
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.3.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
