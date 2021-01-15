mpg123 tones/audiocheck.net_sin_1000Hz_-3dBFS_0.1s.mp3 & sleep 0,571428571

while [ True ] #final version stays stuck in this loop
do
  mpg123 tones/audiocheck.net_sin_3000Hz_-3dBFS_0.1s.mp3 & sleep 0,571428571
done

while [ True ]
do
  mpg123 tones/audiocheck.net_sin_3000Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_3000Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_3000Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_3000Hz_-3dBFS_0.1s.mp3 & sleep 1
done

while [ True ]
do
  mpg123 tones/audiocheck.net_sin_500Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 1
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 1
done

while [ True ]
do
  mpg123 tones/audiocheck.net_sin_500Hz_-3dBFS_0.1s.mp3 & sleep 0.57142857142
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 0.57142857142
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 0.57142857142
  mpg123 tones/audiocheck.net_sin_600Hz_-3dBFS_0.1s.mp3 & sleep 0.57142857142
done
