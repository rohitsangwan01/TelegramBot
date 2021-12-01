import time


def MessageFormat(Title, Size, progress, timeSpent, speed, current, progressV):
    return f"**Title** : {Title}"+"\n"+f"**Size** : {Size}"+"\n" + f"**progress** : {progress}" + "\n" + f"**Downloaded** : {current}" + "\n" + f"**Time** : {timeSpent}"+"\n" + f"**Speed** : {speed}"+"\n"+progressV


def ProgressView(current):
    rangeData = int(100/5)
    currentData = int(current/5)
    ProgressData = ""
    for index in range(rangeData):
        if(index < currentData):
            ProgressData = ProgressData+"●"
        else:
            ProgressData = ProgressData+"○"
    return ProgressData


class ShowProgress():
    waitTime = 0

    def progress(self, current, total, title, size, sentm, startTime):
        if(self.waitTime == 0):
            self.waitTime = time.perf_counter() - startTime

        totalTime = (time.perf_counter() - startTime) - self.waitTime
        CurrentMB = current/1000000

        TimeElapsed = f"{totalTime:.1f} seconds"
        Speed = f"{CurrentMB/totalTime:.1f} Mbps"

        ProgressData = f"{current * 100 / total:.1f}%"
        progressV = ProgressView(current * 100 / total)
        UpdatedStatus = MessageFormat(
            title, f"{size/1000000:.1f} Mb", ProgressData, TimeElapsed, Speed, f"{CurrentMB:.1f} Mb", progressV)
        sentm.edit(UpdatedStatus)
