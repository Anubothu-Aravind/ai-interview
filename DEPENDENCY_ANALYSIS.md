# Dependency Analysis

## Overview

This document provides a comprehensive analysis of all dependencies in the AI Interview System, including their usage, security considerations, and recommendations for optimization.

## Dependency Summary

### Active Dependencies (Currently Used)

| Package | Version | Purpose | Usage Location | Critical |
|---------|---------|---------|----------------|----------|
| streamlit | ≥1.52.2 | Web UI framework | All UI files | ✅ Yes |
| openai | ≥2.14.0 | AI services (GPT-4, Whisper, TTS) | `openai_client.py`, `audio.py` | ✅ Yes |
| supabase | ≥2.27.0 | Database & backend | `database.py` | ✅ Yes |
| python-dotenv | ≥1.2.1 | Environment variable management | `config.py` | ✅ Yes |
| pypdf2 | ≥3.0.1 | PDF text extraction | `utils.py` | ✅ Yes |
| sounddevice | ≥0.5.3 | Audio recording | `audio.py` | ✅ Yes |
| scipy | ≥1.16.3 | WAV file writing | `audio.py` | ✅ Yes |
| numpy | ≥2.4.0 | Audio data manipulation | `audio.py` | ✅ Yes |
| matplotlib | ≥3.10.8 | Waveform visualization | `audio.py` | ⚠️ Optional |

### Deprecated/Unused Dependencies

| Package | Version | Status | Reason | Recommendation |
|---------|---------|--------|--------|----------------|
| gtts | ≥2.5.4 | ❌ Deprecated | Replaced by OpenAI TTS | Remove |
| speechrecognition | ≥3.14.4 | ❌ Deprecated | Replaced by OpenAI Whisper | Remove |
| pyaudio | ≥0.2.14 | ❌ Unused | Using sounddevice instead | Remove |
| pydub | ≥0.25.1 | ❌ Unused | No audio format conversion needed | Remove |
| anthropic | ≥0.75.0 | ❌ Unused | Not integrated, likely for future use | Remove or integrate |
| plotly | ≥6.5.0 | ❌ Unused | Not used for visualization | Remove or use |
| pandas | ≥2.3.3 | ❌ Unused | No data analysis in current code | Remove or use |
| psycopg2-binary | ≥2.9.11 | ❌ Unused | Using Supabase client, not direct PostgreSQL | Remove |

## Detailed Dependency Analysis

### 1. Streamlit (≥1.52.2)

**Purpose**: Primary web application framework

**Usage**:
- `st.set_page_config()` - Page configuration
- `st.markdown()` - HTML/CSS rendering
- `st.session_state` - Session management
- `st.file_uploader()` - File uploads
- `st.button()`, `st.text_input()`, etc. - UI components
- `st.cache_resource` - Resource caching
- `st.audio()` - Audio playback

**Security Considerations**:
- ✅ Generally safe, well-maintained
- ⚠️ No built-in authentication
- ⚠️ Session state stored in memory (not encrypted)

**Alternatives**: 
- FastAPI + React (more scalable)
- Gradio (simpler, less customizable)
- Dash (Plotly-based)

**Recommendation**: ✅ Keep - Core framework

---

### 2. OpenAI (≥2.14.0)

**Purpose**: AI services (GPT-4, Whisper, TTS)

**Usage**:
```python
# GPT-4 for Q&A
client.chat.completions.create(model="gpt-4", ...)

# Whisper for speech-to-text
client.audio.transcriptions.create(model="whisper-1", ...)

# TTS for text-to-speech
client.audio.speech.create(model="tts-1", voice="alloy", ...)
```

**Cost Analysis** (per interview, 10 questions):
- GPT-4 question generation: ~10 calls × $0.03/1K tokens ≈ $0.30
- GPT-4 answer evaluation: ~10 calls × $0.03/1K tokens ≈ $0.30
- Whisper transcription: ~10 calls × $0.006/minute ≈ $0.30 (5min/answer)
- TTS: ~10 calls × $0.015/1K chars ≈ $0.15
- **Total per interview**: ~$1.05

**Security Considerations**:
- ✅ API key stored in environment variable
- ⚠️ No rate limiting implemented
- ⚠️ Potential for API abuse
- ⚠️ No retry logic for failed API calls

**Optimization Opportunities**:
- Use GPT-3.5-turbo for question generation (70% cost reduction)
- Implement response caching for similar resumes/JDs
- Add streaming for faster user feedback
- Implement exponential backoff for retries

**Recommendation**: ✅ Keep - Critical for AI functionality

---

### 3. Supabase (≥2.27.0)

**Purpose**: PostgreSQL database and backend services

**Usage**:
```python
# Query operations
supabase.table('interviews').select('*').execute()
supabase.table('interviews').insert({...}).execute()
supabase.table('questions').eq('interview_id', id).execute()
```

**Features Used**:
- PostgreSQL database (via REST API)
- Auto-generated UUIDs
- Foreign key relationships
- Cascade deletion

**Features NOT Used**:
- Authentication (Supabase Auth)
- Storage (file storage)
- Realtime subscriptions
- Row Level Security (RLS)

**Security Considerations**:
- ⚠️ Using service role key (full access)
- ❌ No Row Level Security enabled
- ❌ No user authentication
- ✅ Connection timeout configured (30s)

**Cost**: Free tier up to 500MB database, 2GB bandwidth/month

**Recommendation**: ✅ Keep - But implement Auth + RLS for production

---

### 4. Python-dotenv (≥1.2.1)

**Purpose**: Load environment variables from `.env` file

**Usage**:
```python
from dotenv import load_dotenv
load_dotenv()
os.getenv("OPENAI_API_KEY")
```

**Security Considerations**:
- ✅ `.env` file is gitignored
- ✅ Prevents hardcoding secrets
- ⚠️ Env file readable if server compromised

**Alternatives**:
- Cloud secret managers (AWS Secrets Manager, GCP Secret Manager)
- Streamlit Secrets (built-in)
- HashiCorp Vault

**Recommendation**: ✅ Keep - Standard practice for local development

---

### 5. PyPDF2 (≥3.0.1)

**Purpose**: Extract text from PDF files (resumes, job descriptions)

**Usage**:
```python
reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
text = "".join(page.extract_text() for page in reader.pages)
```

**Limitations**:
- ❌ No OCR (images not extracted)
- ❌ Complex layouts may break
- ❌ No table extraction
- ✅ Works for simple text PDFs

**Security Considerations**:
- ⚠️ Potential for malicious PDFs
- ❌ No file size validation
- ❌ No content sanitization

**Alternatives**:
- `pdfplumber` - Better table support
- `pymupdf` (fitz) - Faster, more features
- `pdfminer.six` - Better for complex layouts
- Cloud OCR (Google Vision, AWS Textract) - For scanned docs

**Recommendation**: 
- ✅ Keep for MVP
- 🔄 Consider upgrade to `pymupdf` for better performance
- ⚠️ Add file size validation (max 10MB)

---

### 6. Sounddevice (≥0.5.3)

**Purpose**: Real-time audio recording from microphone

**Usage**:
```python
audio = sd.rec(
    int(CHUNK_SECONDS * SAMPLE_RATE),
    samplerate=16000,
    channels=1,
    dtype='float32'
)
sd.wait()
```

**System Requirements**:
- Requires PortAudio library (system-level)
- Microphone permissions
- Works cross-platform (Windows, macOS, Linux)

**Security Considerations**:
- ✅ Local recording only
- ⚠️ Requires browser microphone permission
- ⚠️ Audio data stored in session state (memory)

**Alternatives**:
- `pyaudio` - More common but harder to install
- Browser-based recording (MediaRecorder API)

**Recommendation**: ✅ Keep - Reliable cross-platform solution

---

### 7. SciPy (≥1.16.3)

**Purpose**: Write audio data to WAV files for Whisper API

**Usage**:
```python
from scipy.io.wavfile import write
write(tmp_path, SAMPLE_RATE, audio_int16)
```

**Minimal Usage**: Only uses `scipy.io.wavfile.write`

**Alternatives**:
- `wave` module (Python standard library) - lighter
- `soundfile` - More formats

**Recommendation**: 
- 🔄 Consider replacing with standard library `wave` module
- Reduces dependency weight significantly

**Example replacement**:
```python
import wave
with wave.open(tmp_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio_int16.tobytes())
```

---

### 8. NumPy (≥2.4.0)

**Purpose**: Audio data manipulation and array operations

**Usage**:
```python
# Concatenate audio chunks
audio = np.concatenate(st.session_state.audio_frames, axis=0)

# Convert float32 to int16
audio_int16 = (audio * 32767).astype(np.int16)
```

**Security Considerations**:
- ✅ No security risks
- ⚠️ Large version (100MB+)

**Alternatives**:
- Native Python arrays (much slower)
- No practical alternative for audio processing

**Recommendation**: ✅ Keep - Essential for audio manipulation

---

### 9. Matplotlib (≥3.10.8)

**Purpose**: Waveform visualization during recording

**Usage**:
```python
fig, ax = plt.subplots(figsize=(6, 2))
ax.plot(audio, linewidth=0.5, color='#1f77b4')
st.pyplot(fig)
```

**Concerns**:
- ⚠️ Heavy dependency (~50MB)
- ⚠️ Used only for simple line plot
- ⚠️ Figure recreation every second (performance)

**Alternatives**:
- Plotly (already in dependencies, more interactive)
- Streamlit native charts (`st.line_chart()`)
- Canvas-based rendering (lighter)

**Recommendation**: 
- 🔄 Consider replacing with Plotly or `st.line_chart()`
- Would reduce package size and improve performance

**Example replacement**:
```python
import plotly.graph_objects as go

audio = np.concatenate(st.session_state.audio_frames, axis=0)
fig = go.Figure(go.Scatter(y=audio[:, 0], mode='lines', line=dict(width=0.5)))
fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig)
```

---

## Unused Dependencies - Detailed Analysis

### 10. gTTS (≥2.5.4) - ❌ REMOVE

**Original Purpose**: Google Text-to-Speech

**Why Deprecated**: 
- Replaced by OpenAI TTS in `audio.py`
- OpenAI TTS has better voice quality
- Consistency with OpenAI ecosystem

**Found in code**: 
- `app/app.py` (deprecated monolithic file)

**Recommendation**: ✅ Remove from `pyproject.toml` and `requirements.txt`

---

### 11. SpeechRecognition (≥3.14.4) - ❌ REMOVE

**Original Purpose**: Google Speech Recognition

**Why Deprecated**:
- Replaced by OpenAI Whisper
- Whisper has better accuracy
- Consistency with OpenAI ecosystem

**Found in code**: 
- `app/app.py` (deprecated monolithic file)

**Recommendation**: ✅ Remove from `pyproject.toml` and `requirements.txt`

---

### 12. PyAudio (≥0.2.14) - ❌ REMOVE

**Original Purpose**: Audio recording

**Why Unused**: 
- Using `sounddevice` instead
- Easier installation across platforms

**Found in code**: Nowhere (fully replaced)

**Recommendation**: ✅ Remove from `pyproject.toml` and `requirements.txt`

---

### 13. Pydub (≥0.25.1) - ❌ REMOVE

**Original Purpose**: Audio format conversion

**Why Unused**: 
- No format conversion needed
- Direct WAV output to Whisper API

**Found in code**: Nowhere

**Recommendation**: ✅ Remove from `pyproject.toml` and `requirements.txt`

---

### 14. Anthropic (≥0.75.0) - ⚠️ DECISION NEEDED

**Purpose**: Claude AI integration

**Current Status**: Not used in codebase

**Potential Use Cases**:
- Alternative to OpenAI GPT-4
- A/B testing different AI models
- Cost optimization (Claude may be cheaper)
- Redundancy if OpenAI is down

**Recommendation**: 
- ❌ Remove if no plans to integrate
- ✅ Keep if planning Claude integration
- 🔄 Document decision in roadmap

---

### 15. Plotly (≥6.5.0) - 🔄 USE OR REMOVE

**Purpose**: Interactive visualizations

**Current Status**: Listed but not used

**Potential Use Cases**:
- Replace Matplotlib for waveform (lighter, more interactive)
- Analytics dashboard for interview statistics
- Score distribution charts

**Recommendation**: 
- ✅ Use to replace Matplotlib (see Matplotlib section above)
- OR ❌ Remove if not planning to use

---

### 16. Pandas (≥2.3.3) - 🔄 USE OR REMOVE

**Purpose**: Data manipulation and analysis

**Current Status**: Listed but not used

**Potential Use Cases**:
- Interview analytics (average scores, trends)
- Export to Excel/CSV
- Data aggregation for dashboards

**Recommendation**: 
- ✅ Use for analytics features
- OR ❌ Remove if not planning analytics

---

### 17. psycopg2-binary (≥2.9.11) - ❌ REMOVE

**Purpose**: Direct PostgreSQL connection

**Why Unused**: 
- Using Supabase Python client (REST API)
- No direct SQL queries in codebase

**Note**: Supabase client uses HTTP, not direct Postgres connection

**Recommendation**: ✅ Remove - Not needed with Supabase client

---

## Security Vulnerabilities Check

### Known CVEs (as of 2026-01-01)

| Package | Version | Known Issues | Severity | Mitigation |
|---------|---------|--------------|----------|------------|
| streamlit | 1.52.2 | None major | - | Keep updated |
| openai | 2.14.0 | None | - | Keep updated |
| numpy | 2.4.0 | None | - | Keep updated |
| PyPDF2 | 3.0.1 | Potential DoS with malicious PDFs | Medium | Add file size limits, sanitization |

**Recommendation**: 
- ✅ All dependencies are relatively recent
- ⚠️ Add file size validation for PDF uploads
- ✅ Keep dependencies updated regularly

---

## Dependency Size Analysis

Estimated package sizes (unpacked):

| Package | Size | Category |
|---------|------|----------|
| streamlit | ~50 MB | Large |
| openai | ~5 MB | Small |
| matplotlib | ~50 MB | Large |
| numpy | ~100 MB | Large |
| scipy | ~60 MB | Large |
| plotly | ~30 MB | Medium |
| pandas | ~60 MB | Large (unused) |
| supabase | ~5 MB | Small |
| sounddevice | ~1 MB | Small |
| pypdf2 | ~5 MB | Small |

**Total (with all deps)**: ~366 MB
**Total (optimized, removing unused)**: ~276 MB (24% reduction)

---

## Recommended Dependency Optimization

### Phase 1: Remove Unused (Immediate)

```toml
# Remove from pyproject.toml
# - gtts
# - speechrecognition
# - pyaudio
# - pydub
# - psycopg2-binary
```

**Impact**: 
- Cleaner dependencies
- Faster installation
- Reduced attack surface

---

### Phase 2: Decision on Optional (Next Sprint)

**Option A - Analytics Focus**:
```toml
# Keep and use:
# - plotly (replace matplotlib)
# - pandas (add analytics)
# Remove:
# - anthropic
# - matplotlib
```

**Option B - Minimal**:
```toml
# Remove:
# - anthropic
# - plotly
# - pandas
# Optimize matplotlib usage
```

---

### Phase 3: Optimize Heavy Dependencies (Future)

1. **Replace SciPy with standard library `wave`**
   - Reduce 60MB dependency
   - Only need WAV writing functionality

2. **Replace Matplotlib with Plotly** (if keeping Plotly)
   - Already in dependencies
   - More interactive
   - Better Streamlit integration

3. **Consider PyMuPDF instead of PyPDF2**
   - Faster PDF parsing
   - Better table support
   - Similar size

---

## Final Optimized Dependency List

### Recommended Production Dependencies

```toml
[project]
dependencies = [
    "streamlit>=1.52.2",        # Web UI framework
    "openai>=2.14.0",           # AI services
    "supabase>=2.27.0",         # Database
    "python-dotenv>=1.2.1",     # Environment config
    "pypdf2>=3.0.1",            # PDF parsing (or pymupdf)
    "sounddevice>=0.5.3",       # Audio recording
    "numpy>=2.4.0",             # Array operations
    "plotly>=6.5.0",            # Visualization (replace matplotlib)
    "pandas>=2.3.3",            # Analytics (if needed)
]
```

**Removed**: gtts, speechrecognition, pyaudio, pydub, psycopg2-binary, anthropic, matplotlib, scipy

**Added functionality**:
- Use `wave` module instead of scipy
- Use Plotly instead of Matplotlib

**Size Reduction**: ~140 MB (38% reduction)

---

## Version Management Strategy

### Current Strategy
- Minimum version constraints (`>=`)
- No upper bounds
- Potential breaking changes in major updates

### Recommended Strategy

```toml
# Pin major versions to prevent breaking changes
dependencies = [
    "streamlit>=1.52.2,<2.0",
    "openai>=2.14.0,<3.0",
    "supabase>=2.27.0,<3.0",
    # ... etc
]
```

**Benefits**:
- Prevent unexpected breaking changes
- Allow minor/patch updates for security
- Clear upgrade path

---

## Dependency Update Process

### Recommended Update Cadence

1. **Security patches**: Immediately
2. **Minor versions**: Monthly review
3. **Major versions**: Quarterly review with testing

### Update Checklist

```bash
# 1. Check for updates
pip list --outdated

# 2. Review changelogs for breaking changes

# 3. Update in dev environment
pip install -U <package>

# 4. Run tests
python -m pytest

# 5. Update lock file
uv lock

# 6. Update pyproject.toml

# 7. Deploy to staging

# 8. Deploy to production
```

---

## Development vs Production Dependencies

### Current State
- No separation between dev and prod dependencies

### Recommended Structure

```toml
[project]
dependencies = [
    # Production only
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

**Installation**:
```bash
# Production
pip install .

# Development
pip install ".[dev]"
```

---

## Conclusion

### Summary of Recommendations

1. **Remove immediately**: gtts, speechrecognition, pyaudio, pydub, psycopg2-binary
2. **Decide within 1 sprint**: anthropic, plotly, pandas (use or remove)
3. **Optimize in future**: Replace scipy with `wave`, matplotlib with plotly
4. **Add security**: File size limits, input validation
5. **Implement**: Version pinning, dev/prod separation
6. **Establish**: Regular update cadence

### Expected Benefits

- **38% smaller installation** (~140MB saved)
- **Faster deployment** (fewer packages to install)
- **Better security** (reduced attack surface)
- **Clearer purpose** (every dependency justified)
- **Easier maintenance** (fewer updates to track)

### Risk Assessment

- ✅ Low Risk: Removing unused dependencies
- ✅ Low Risk: Replacing scipy with `wave`
- ⚠️ Medium Risk: Replacing matplotlib with plotly (requires testing)
- ⚠️ Medium Risk: Major version upgrades (requires comprehensive testing)
