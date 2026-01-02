import { formatTime, AudioRecorder } from './audio';

describe('formatTime', () => {
  it('should format seconds correctly', () => {
    expect(formatTime(0)).toBe('0:00');
    expect(formatTime(30)).toBe('0:30');
    expect(formatTime(60)).toBe('1:00');
    expect(formatTime(90)).toBe('1:30');
    expect(formatTime(300)).toBe('5:00');
  });

  it('should pad single digit seconds', () => {
    expect(formatTime(5)).toBe('0:05');
    expect(formatTime(65)).toBe('1:05');
  });
});

describe('AudioRecorder', () => {
  it('should create an instance', () => {
    const recorder = new AudioRecorder();
    expect(recorder).toBeInstanceOf(AudioRecorder);
  });

  it('should report not recording initially', () => {
    const recorder = new AudioRecorder();
    expect(recorder.isRecording()).toBe(false);
  });
});
