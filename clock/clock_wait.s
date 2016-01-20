// On utilise les registres suivants :
// Minutes : %r04
// Heures : %r05
// Jours : %r06
// Mois : %r07
// Année : %r08
// Siècle : %r09
// Nombre de jours dans le mois : %r10
// Temp : %r11
// Buffer de sortie 1 : %r12
// Buffer de sortie 2 : %r13

// Initialisation

	JMP init

// La boucle principale :
// L'incrémentation des secondes est entièrement déroulée,
//  elle s'exécute exactement une instruction sur deux.
// On récupère le reste du temps pour calculer l'affichage
//  suivant, qui remplacera l'actuel à la fin de la boucle.
loop:
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	MOV %r12, #0x3939 // {00}
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	// Début du calcul du nombre de jours dans le mois
	// tmp = mois + 100 (addresse des durées)
	ADD %r11, %r07, #100
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	// jours_mois = mem[tmp]
	LDR %r10, %r11
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	// tmp = année ; on set les flags
	ADDS %r11, %r08, #0
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	// Si année == 0, tmp = siècle
	MOVEQ %r11, %r09
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	// L'année est bissextile ssi tmp % 4 == 0
	TST %r11, #3
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	// On teste le mois aussi
	TEQEQ %r07, #2
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	// Maintenant, on a Z ssi l'année est bissextile
	//  et on est en février
	ADDEQ %r10, %r10, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	// On ajoute une minute
	ADD %r04, %r04, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x3950 // {09} ^ {10}
	// Minutes == 60 ?
	TEQ %r04, #60
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	// On reset les minutes
	MOVEQ %r04, #0
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	// On incrémente les heures
	ADDEQ %r05, %r05, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	// Heures == 24 ?
	TEQ %r05, #24
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	// On reset les heures
	MOVEQ %r05, #0
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	// On incrémente les jours
	ADDEQ %r06, %r06, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	// Jours == jours_mois + 1 ?
	TEQ %r06, %r10
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	// On reset les jours
	MOVEQ %r06, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	// On incrémente les mois
	ADDEQ %r07, %r07, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	// Mois == 13 ?
	TEQ %r07, #13
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d50 // {19} ^ {20}
	// On reset les mois
	MOVEQ %r07, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	// On incrémente les années
	ADDEQ %r08, %r08, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	// Années == 100 ?
	TEQ %r08, #100
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	// On reset les années
	MOVEQ %r08, #0
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	// On incrémente les siècles
	ADDEQ %r09, %r09, #1
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	// Siècle == 100 ?
	TEQ %r09, #100
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	// On reset les siècles
	MOVEQ %r09, #0
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	// On charge les nouvelles valeurs dans les buffers
	LDR %r11, %r04
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	ORR %r12, %r12, %r11, LSL #16
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	LDR %r11, %r05
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x1450 // {29} ^ {30}
	ORR %r12, %r12, %r11, LSL #32
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	LDR %r13, %r06
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	LDR %r11, %r07
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	ORR %r13, %r13, %r11, LSL #16
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	LDR %r11, %r08
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	ORR %r13, %r13, %r11, LSL #32
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	LDR %r11, %r09
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	ORR %r13, %r13, %r11, LSL #48
	// Maintenant, %r12 et %r13 contiennent les nouvelles
	//  valeurs à mettre dans %r02 et %r03
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x2950 // {39} ^ {40}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b50 // {49} ^ {50}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x39 // {0} ^ {1}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x5d // {1} ^ {2}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x14 // {2} ^ {3}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x29 // {3} ^ {4}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x0b // {4} ^ {5}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {5} ^ {6}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x7a // {6} ^ {7}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x78 // {7} ^ {8}
	ADD %r15, %r15, #0 // NOP
	ADD %r00, %r00, %r01 // Wait
	EOR %r02, %r02, #0x10 // {8} ^ {9}
	ADD %r00, %r00, %r01 // Wait
	// On met à jour date
	MOV %r03, %r13
	// On met à jour minutes/heure
	MOV %r02, %r12
	// Et c'est reparti !
	JMP loop

init:
	MOV %r04, #0
	MOV %r05, #0
	MOV %r06, #1
	MOV %r07, #1
	MOV %r08, #0
	MOV %r09, #0
	// Initialisation de la sortie
	MOV %r11, #0x3f3f // 00
	ORR %r11, %r11, #0x3f3f, LSL #16
	ORR %r02, %r11, #0x3f3f, LSL #32
	MOV %r11, #0x3f06 // 01
	ORR %r11, %r11, #0x3f06, LSL #16
	ORR %r03, %r11, %r02, LSL #32 // On a maintenant 00000101 dans r03
	// Initialisation de la table
	MOV %r11, #0x3f3f // 00
	STR %r11, #00
	MOV %r11, #0x3f06 // 01
	STR %r11, #01
	MOV %r11, #0x3f5b // 02
	STR %r11, #02
	MOV %r11, #0x3f4f // 03
	STR %r11, #03
	MOV %r11, #0x3f66 // 04
	STR %r11, #04
	MOV %r11, #0x3f6d // 05
	STR %r11, #05
	MOV %r11, #0x3f7d // 06
	STR %r11, #06
	MOV %r11, #0x3f07 // 07
	STR %r11, #07
	MOV %r11, #0x3f7f // 08
	STR %r11, #08
	MOV %r11, #0x3f6f // 09
	STR %r11, #09
	MOV %r11, #0x063f // 10
	STR %r11, #10
	MOV %r11, #0x0606 // 11
	STR %r11, #11
	MOV %r11, #0x065b // 12
	STR %r11, #12
	MOV %r11, #0x064f // 13
	STR %r11, #13
	MOV %r11, #0x0666 // 14
	STR %r11, #14
	MOV %r11, #0x066d // 15
	STR %r11, #15
	MOV %r11, #0x067d // 16
	STR %r11, #16
	MOV %r11, #0x0607 // 17
	STR %r11, #17
	MOV %r11, #0x067f // 18
	STR %r11, #18
	MOV %r11, #0x066f // 19
	STR %r11, #19
	MOV %r11, #0x5b3f // 20
	STR %r11, #20
	MOV %r11, #0x5b06 // 21
	STR %r11, #21
	MOV %r11, #0x5b5b // 22
	STR %r11, #22
	MOV %r11, #0x5b4f // 23
	STR %r11, #23
	MOV %r11, #0x5b66 // 24
	STR %r11, #24
	MOV %r11, #0x5b6d // 25
	STR %r11, #25
	MOV %r11, #0x5b7d // 26
	STR %r11, #26
	MOV %r11, #0x5b07 // 27
	STR %r11, #27
	MOV %r11, #0x5b7f // 28
	STR %r11, #28
	MOV %r11, #0x5b6f // 29
	STR %r11, #29
	MOV %r11, #0x4f3f // 30
	STR %r11, #30
	MOV %r11, #0x4f06 // 31
	STR %r11, #31
	MOV %r11, #0x4f5b // 32
	STR %r11, #32
	MOV %r11, #0x4f4f // 33
	STR %r11, #33
	MOV %r11, #0x4f66 // 34
	STR %r11, #34
	MOV %r11, #0x4f6d // 35
	STR %r11, #35
	MOV %r11, #0x4f7d // 36
	STR %r11, #36
	MOV %r11, #0x4f07 // 37
	STR %r11, #37
	MOV %r11, #0x4f7f // 38
	STR %r11, #38
	MOV %r11, #0x4f6f // 39
	STR %r11, #39
	MOV %r11, #0x663f // 40
	STR %r11, #40
	MOV %r11, #0x6606 // 41
	STR %r11, #41
	MOV %r11, #0x665b // 42
	STR %r11, #42
	MOV %r11, #0x664f // 43
	STR %r11, #43
	MOV %r11, #0x6666 // 44
	STR %r11, #44
	MOV %r11, #0x666d // 45
	STR %r11, #45
	MOV %r11, #0x667d // 46
	STR %r11, #46
	MOV %r11, #0x6607 // 47
	STR %r11, #47
	MOV %r11, #0x667f // 48
	STR %r11, #48
	MOV %r11, #0x666f // 49
	STR %r11, #49
	MOV %r11, #0x6d3f // 50
	STR %r11, #50
	MOV %r11, #0x6d06 // 51
	STR %r11, #51
	MOV %r11, #0x6d5b // 52
	STR %r11, #52
	MOV %r11, #0x6d4f // 53
	STR %r11, #53
	MOV %r11, #0x6d66 // 54
	STR %r11, #54
	MOV %r11, #0x6d6d // 55
	STR %r11, #55
	MOV %r11, #0x6d7d // 56
	STR %r11, #56
	MOV %r11, #0x6d07 // 57
	STR %r11, #57
	MOV %r11, #0x6d7f // 58
	STR %r11, #58
	MOV %r11, #0x6d6f // 59
	STR %r11, #59
	MOV %r11, #0x7d3f // 60
	STR %r11, #60
	MOV %r11, #0x7d06 // 61
	STR %r11, #61
	MOV %r11, #0x7d5b // 62
	STR %r11, #62
	MOV %r11, #0x7d4f // 63
	STR %r11, #63
	MOV %r11, #0x7d66 // 64
	STR %r11, #64
	MOV %r11, #0x7d6d // 65
	STR %r11, #65
	MOV %r11, #0x7d7d // 66
	STR %r11, #66
	MOV %r11, #0x7d07 // 67
	STR %r11, #67
	MOV %r11, #0x7d7f // 68
	STR %r11, #68
	MOV %r11, #0x7d6f // 69
	STR %r11, #69
	MOV %r11, #0x073f // 70
	STR %r11, #70
	MOV %r11, #0x0706 // 71
	STR %r11, #71
	MOV %r11, #0x075b // 72
	STR %r11, #72
	MOV %r11, #0x074f // 73
	STR %r11, #73
	MOV %r11, #0x0766 // 74
	STR %r11, #74
	MOV %r11, #0x076d // 75
	STR %r11, #75
	MOV %r11, #0x077d // 76
	STR %r11, #76
	MOV %r11, #0x0707 // 77
	STR %r11, #77
	MOV %r11, #0x077f // 78
	STR %r11, #78
	MOV %r11, #0x076f // 79
	STR %r11, #79
	MOV %r11, #0x7f3f // 80
	STR %r11, #80
	MOV %r11, #0x7f06 // 81
	STR %r11, #81
	MOV %r11, #0x7f5b // 82
	STR %r11, #82
	MOV %r11, #0x7f4f // 83
	STR %r11, #83
	MOV %r11, #0x7f66 // 84
	STR %r11, #84
	MOV %r11, #0x7f6d // 85
	STR %r11, #85
	MOV %r11, #0x7f7d // 86
	STR %r11, #86
	MOV %r11, #0x7f07 // 87
	STR %r11, #87
	MOV %r11, #0x7f7f // 88
	STR %r11, #88
	MOV %r11, #0x7f6f // 89
	STR %r11, #89
	MOV %r11, #0x6f3f // 90
	STR %r11, #90
	MOV %r11, #0x6f06 // 91
	STR %r11, #91
	MOV %r11, #0x6f5b // 92
	STR %r11, #92
	MOV %r11, #0x6f4f // 93
	STR %r11, #93
	MOV %r11, #0x6f66 // 94
	STR %r11, #94
	MOV %r11, #0x6f6d // 95
	STR %r11, #95
	MOV %r11, #0x6f7d // 96
	STR %r11, #96
	MOV %r11, #0x6f07 // 97
	STR %r11, #97
	MOV %r11, #0x6f7f // 98
	STR %r11, #98
	MOV %r11, #0x6f6f // 99
	STR %r11, #99
	MOV %r11, #32
	STR %r11, #101
	STR %r11, #103
	STR %r11, #105
	STR %r11, #107
	STR %r11, #108
	STR %r11, #110
	STR %r11, #112
	MOV %r11, #29
	STR %r11, #102
	MOV %r11, #31
	STR %r11, #104
	STR %r11, #106
	STR %r11, #109
	STR %r11, #111
	JMP loop

// mn = minutes
// h = heures
// j = jours
// mo = mois
// y = année
// si = siècle
// MOV out_buffer1 #{00}
// Calcul du nombre de jours dans le mois:
// ADD tmp mo #100
// LDR mj [tmp]
// MOV tmp y
// TEQ y #0
// MOVEQ tmp si
// TST tmp #3
// -- On a Z ssi l'année est bissextile
// TEQEQ mo #2
// -- Maintenant, ssi bissextile ET on est en février
// ADDEQ mj #1
// ADD mn mn #1
// TEQ mn #60
// MOVEQ mn #0
// ADDEQ h h #1
// TEQ h #24
// MOVEQ h #0
// ADDEQ j #1
// TEQ j mj
// MOVEQ j #1
// ADDEQ mo #1
// TEQ mo #13
// MOVEQ mo #1
// ADDEQ y #1
// TEQ y #100
// MOVEQ y #0
// ADDEQ si #1
// TEQ si #100
// MOVEQ si #0
// LDR tmp [mn]
// ORR out_buffer1 out_buffer1 tmp LSL #16
// LDR tmp [h]
// ORR out_buffer1 out_buffer1 tmp LSL #32
// LDR out_buffer2 [j]
// LDR tmp [mo]
// ORR out_buffer2 out_buffer2 tmp LSL #16
// LDR tmp [y]
// ORR out_buffer2 out_buffer2 tmp LSL #32
// LDR tmp [si]
// ORR out_buffer2 out_buffer2 tmp LSL #48
// MOV out_buffer2 out2
