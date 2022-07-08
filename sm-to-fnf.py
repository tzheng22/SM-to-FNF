with open("two.txt", "r") as f:
    two_old = f.read().split(",")
    f.close()

a = 0
two = []
while a < len(two_old) and len(two_old) > 1:
    two.append(two_old[a].replace("\n", ""))
    a += 1

with open("one.txt", "r") as f:
    one_old = f.read().split(",")
    f.close()

b = 0
one = []
while b < len(one_old) and len(one_old) > 1:
    one.append(one_old[b].replace("\n", ""))
    b += 1


while len(two) < len(one):
    two.append("00000000")

while len(one) < len(two):
    one.append("00000000")

newFile = open("newfile.txt", "w")

i = 0
while i < len(one):
    j = 0
    k = 0
    l = 0
    while j < 192:
        snap1 = 192 / (len(one[i]) / 4)
        snap2 = 192 / (len(two[i]) / 4)
        if j % snap1 == 0 and j % snap2 == 0:
            newFile.write(two[i][4 * l:4 * (l + 1)] + one[i][4 * k:4 * (k + 1)] + "\n")
            k += 1
            l += 1
        elif j % snap1 == 0 and j % snap2 != 0:
            newFile.write("0000" + one[i][4 * k:4 * (k + 1)] + "\n")
            k += 1
        elif j % snap1 != 0 and j % snap2 == 0:
            newFile.write(two[i][4 * l:4 * (l + 1)] + "0000" + "\n")
            l += 1
        else:
            newFile.write("00000000\n")
        j += 1
    newFile.write(",\n")
    i += 1

newFile.close()
c = 0
with open("newfile.txt", "r") as f:
    together_old = f.read().split(",")
    f.close()
together = []
while c < len(together_old) - 1:
    together.append(together_old[c].replace("\n", ""))
    c += 1

with open("bpms.txt", "r") as f:
    bpmsTimestamps = f.read().splitlines()

bpm = []
timestamps = []

for i in bpmsTimestamps:
    temp = i.split("=")
    timestamps.append(temp[0])
    bpm.append(temp[1])

m = 0

currentBPM = float(bpm[m])

notes = []
bpmofnotes = []

currBeatInMilliSeconds = 0

currBeat = 0

l = 0
hold = [0, 0, 0, 0, 0, 0, 0, 0]
holdtimestamp = [0, 0, 0, 0, 0, 0, 0, 0]
counthold = [False, False, False, False, False, False, False, False]
firstnote = []
while l < len(together):
    h = 0
    sectionNotes = []
    while h < len(together[l]) / 8:
        x = 0
        if m < len(timestamps) - 1 and float(timestamps[m + 1]) == round(currBeat, 3):
            m += 1
            currentBPM = float(bpm[m])
        millisecondsPerBeat = 60000 / currentBPM
        while x < 8:
            if counthold[x]:
                hold[x] += millisecondsPerBeat / 48
            if together[l][8 * h + x:8 * h + x + 1] == "1":
                sectionNotes.append([currBeatInMilliSeconds, x, 0, 0])
            elif together[l][8 * h + x:8 * h + x + 1] == "M":
                sectionNotes.append([currBeatInMilliSeconds, x, 0, 3])
            elif together[l][8 * h + x:8 * h + x + 1] == "2":
                counthold[x] = True
                holdtimestamp[x] = currBeatInMilliSeconds
            elif together[l][8 * h + x:8 * h + x + 1] == "3":
                counthold[x] = False
                o = 0
                q = 0
                p = 0
                if len(notes) > 0:
                    if len(notes[o]) > 0:
                        while o < len(notes):
                            p = 0
                            while p < len(notes[o]) and holdtimestamp[x] > notes[o][p][0]:
                                p += 1
                            if p < len(notes[o]):
                                q = p
                                break
                            o += 1
                        if o == len(notes):
                            sectionNotes.append([holdtimestamp[x], x, hold[x], 0])
                        else:
                            notes[o].insert(q, [holdtimestamp[x], x, hold[x], 0])
                    else:
                        sectionNotes.append([holdtimestamp[x], x, hold[x], 0])
                else:
                    sectionNotes.append([holdtimestamp[x], x, hold[x], 0])
                hold[x] = 0
                holdtimestamp[x] = 0
            x += 1
        currBeatInMilliSeconds += millisecondsPerBeat / 48
        currBeat += 1 / 48
        h += 1
    changeBPM = m > 0 and currentBPM != bpm[m - 1]
    if changeBPM:
        changeBPM = "true"
    else:
        changeBPM = "false"
    bpmofnotes.append([currentBPM, changeBPM])
    notes.append(sectionNotes)
    l += 1

note = []
u = 0
while u < len(notes):
    if u < len(notes) - 1:
        note.append("{\n" + f"\"sectionNotes\":{str(notes[u])},\n\"lengthInSteps\": 16,\n\"bpm\": {bpmofnotes[u][0]},\n\"changeBPM\": {bpmofnotes[u][1]},\n\"mustHitSection\": false" + "\n},\n")
    else:
        note.append("{\n" + f"\"sectionNotes\":{str(notes[u])},\n\"lengthInSteps\": 16,\n\"bpm\": {bpmofnotes[u][0]},\n\"changeBPM\": {bpmofnotes[u][1]},\n\"mustHitSection\": false" + "\n}\n")
    u += 1
yourMom = input("song name? ").replace(" ", "-")
difficulty = input("difficulty? (blank if normal) ").replace(" ", "-")
if difficulty:
    difficulty = "-" + difficulty
output = open(f"{yourMom + difficulty}.json", "w")
output.write("{\n\"song\": {\n\"sectionLengths\": [],\n\"player1\": \"bf\",\n\"events\": [],\n\"gfVersion\": \"gf\",\n\"notes\": [\n")
for i in note:
    output.write(i)
output.write("],\n\"player2\": \"dad\",\n\"player3\": null,\n\"song\": \"" + yourMom + "\",\n\"validScore\": true,\n\"stage\": \"stage\",\n\"sections\": 0,\n\"needsVoices\": true,\n\"speed\": 3.5,\n" + f"\"bpm\": {bpm[0]}\n" + "}\n}")
output.close()
