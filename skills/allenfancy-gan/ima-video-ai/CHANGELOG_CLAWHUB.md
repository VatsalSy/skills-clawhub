# Changelog — ima-video-ai

All notable changes to this skill are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioned via [Semantic Versioning](https://semver.org/).

---

## v1.0.2 (2026-02-28) — Security Transparency Update

### 🔒 Security & Documentation Improvements

**Enhanced transparency and security disclosure in response to OpenClaw security audit.**

#### Changed
- **Full Network Endpoint Disclosure**: Updated all documentation to explicitly list both domains used:
  - `api.imastudio.com` (main API for task creation and polling)
  - `imapi.liveme.com` (image upload service for i2v tasks)
- **Credential Flow Documentation**: Added detailed explanation of why IMA API key is sent to both domains
- **Security Notice**: Added prominent credential security notice in SKILL.md
- **APP_KEY Disclosure**: Documented hardcoded APP_KEY as shared public key (not a secret)

#### Added
- **Network Traffic Verification Guide**: Step-by-step instructions for monitoring network traffic (SECURITY.md)
- **Security Checklist**: Pre-installation verification steps (INSTALL.md)
- **Domain Ownership Verification**: DNS verification commands for both domains
- **Code Comments**: Enhanced inline documentation explaining upload flow and credential usage
- **clawhub.json**: Updated IMA_API_KEY description to mention both domains

#### Fixed
- Removed false claims that "all requests go to api.imastudio.com only"
- Corrected copy-paste errors referencing "ima_voice_create.py" in INSTALL.md
- Updated test examples to use video generation instead of music

#### Documentation
- SKILL.md: Added "🌐 Network Endpoints Used" and "⚠️ Credential Security Notice" sections
- SECURITY.md: Added "Network Traffic Verification" and "Hardcoded APP_KEY Disclosure" sections
- INSTALL.md: Added "Security Checklist (Before First Use)" section
- CHANGELOG_CLAWHUB.md: Updated technical details to list both API endpoints
- scripts/ima_video_create.py: Enhanced function docstrings with security explanations

**No functional changes** — purely documentation and transparency improvements.

---

## v1.0.1 (2026-02-27) — Initial Release

### 🎬 AI Video Generation via IMA Open API

**Generate professional AI videos from text or images — cinematic quality in minutes.**

Transform text descriptions or images into complete video clips. Whether you need promotional videos, social media content, animated scenes, or cinematic sequences, this skill handles it all through the powerful IMA Open API.

---

### ✨ Key Features

#### 🎥 4 Video Generation Modes

1. **Text to Video** (14 models)
   - Generate videos from text descriptions
   - Cinematic camera movements, scene composition
   - Duration: 4-15 seconds
   - Resolution: 540P to 4K

2. **Image to Video** (14 models)
   - Bring static images to life
   - Camera movements, object animation
   - Preserve image composition while adding motion
   - Duration: 4-15 seconds

3. **First-Last Frame to Video** (10 models)
   - Interpolate smooth transitions between two frames
   - Perfect for morphing effects and transitions
   - Duration: 5-10 seconds

4. **Reference Image to Video** (9 models)
   - Generate videos using reference images for style/composition
   - Maintain character/style consistency
   - Duration: 4-10 seconds

#### 🌟 Production-Ready AI Models

**Most Popular Defaults (Balanced Quality/Cost):**
- **Wan 2.6** (25 pts) — Most popular for both text-to-video and image-to-video
  - 720P/1080P support
  - 5-15 second duration options
  - Fast generation (60-120s)
  - Excellent quality-to-cost ratio

**Premium Options:**
- **Kling O1** (48-120 pts) — Latest Kling reasoning model
  - Newest generation model (2026)
  - Built-in audio generation
  - Superior motion coherence
  - Best for text-to-video and frame interpolation

- **Hailuo 2.3** (38 pts) — Latest MiniMax/Hailuo
  - Higher quality than 2.0
  - 768P resolution
  - 6-second duration

- **Google Veo 3.1** (70-330 pts) — State-of-the-art cinematic quality
  - SOTA model for professional use
  - 720P to 4K resolution
  - 4-8 second duration
  - Exceptional camera work and lighting

**Budget Options:**
- **Vidu Q2** (5-70 pts) — Fastest and most affordable
  - Great for rapid prototyping
  - 540P-1080P
  - 5-10 second duration

**Additional Models:**
- Sora 2 Pro (122+ pts) — OpenAI's premium model
- Kling 2.6 (80+ pts) — Previous generation Kling
- SeeDance 1.5 Pro (20+ pts) — ByteDance/DouBao
- Pixverse V3.5-V5.5 (12-48 pts) — Budget-friendly series

#### 🎯 Smart Features

- **Automatic model selection**: Defaults to newest/most popular model (Wan 2.6)
- **User preference memory**: Remembers your favorite model for each video type
- **Cost transparency**: Shows credits and estimated time before generation
- **Progress tracking**: Real-time updates during 1-6 minute generation
- **Automatic image upload**: Local files automatically uploaded to OSS
- **High-quality output**: MP4 video files with first-frame thumbnail

#### 🔧 Advanced Video Controls

- **Resolution**: 540P, 720P, 1080P, 2K, 4K (model-dependent)
- **Aspect Ratio**: 16:9, 9:16, 1:1, 4:3 (widescreen, vertical, square)
- **Duration**: 4-15 seconds (model-dependent)
- **Shot Type**: Single shot, multi-shot transitions
- **Negative Prompts**: Exclude unwanted elements
- **Prompt Enhancement**: AI-powered prompt optimization
- **Seed Control**: Reproducible results with fixed seeds

---

### 🚀 What You Can Generate

- **Marketing Content**: Product demos, promotional videos, social ads
- **Social Media**: TikTok clips, Instagram Reels, YouTube Shorts
- **Creative Projects**: Music videos, artistic animations, visual effects
- **Business Content**: Presentations, explainer videos, training materials
- **Cinematic Sequences**: Scene transitions, establishing shots, B-roll
- **Animation**: Character movements, object transformations, morphing

---

### 📝 Prompt Examples

#### Text to Video
```
"a cute puppy running across a sunny meadow, cinematic 4K"
→ Adorable pet video with professional camera work

"city skyline at sunset, camera slowly panning right, golden hour lighting"
→ Cinematic establishing shot

"underwater scene with colorful tropical fish, slow motion, coral reef"
→ Nature documentary style

"futuristic neon cityscape, cyberpunk aesthetic, night time, rain reflections"
→ Blade Runner-inspired scene
```

#### Image to Video
```
"camera slowly zooms in"
→ Ken Burns effect on static image

"bring this landscape alive with gentle wind and moving clouds"
→ Subtle animation for photography

"object rotates 360 degrees, studio lighting"
→ Product showcase video
```

#### First-Last Frame to Video
```
"smooth transition between frames"
→ Morphing effect

"character walks from position A to position B, natural motion"
→ Animation interpolation
```

---

### 🎨 Use Cases

| Use Case | Example |
|----------|---------|
| 📱 **Social Media** | TikTok/Instagram Reels, viral content |
| 🎬 **Content Creation** | YouTube videos, thumbnails, B-roll |
| 📢 **Marketing** | Product demos, ads, promotional content |
| 🎮 **Game Dev** | Cinematics, cutscenes, trailers |
| 🏢 **Business** | Presentations, training videos, explainers |
| 🎨 **Creative Arts** | Music videos, art projects, experiments |

---

### 🔐 Security & Best Practices

- **Read-only skill**: No modifications allowed — ensures reliability and security
- **API key required**: Set `IMA_API_KEY` environment variable
- **Automatic updates**: Always uses latest API endpoints and model versions
- **Production-validated**: Tested on real IMA Open API infrastructure
- **Image upload security**: Automatic OSS upload with secure token generation

---

### 📊 Technical Details

- **API Endpoints**: 
  - Main API: `https://api.imastudio.com` (task creation, status polling)
  - Upload Service: `https://imapi.liveme.com` (image uploads for i2v tasks)
- **Authentication**: Bearer token (`ima_*` API key)
- **Task Types**: `text_to_video`, `image_to_video`, `first_last_frame_to_video`, `reference_image_to_video`
- **Output Format**: MP4 video files + JPEG thumbnail (first frame)
- **Generation Time**: 
  - Wan 2.6: 60-120 seconds
  - Kling O1: 180-360 seconds
  - Vidu Q2: 60-120 seconds
  - Google Veo 3.1: 120-300 seconds
- **Poll Interval**: 8 seconds (optimized for video generation)
- **Quality**: Professional-grade video suitable for commercial use

---

### 🎯 Why Choose This Skill?

✅ **Always up-to-date**: Automatically queries latest models from IMA API  
✅ **Smart defaults**: Recommends newest & most popular models, not cheapest  
✅ **User-friendly**: No technical knowledge required — just describe what you want  
✅ **Cost-efficient**: Transparent credit usage, from 5 to 330 points per generation  
✅ **Production-ready**: Used by real businesses and content creators  
✅ **Comprehensive**: Supports all major AI video generation engines  
✅ **Automatic image handling**: Local files uploaded seamlessly

---

### 🏷️ Tags

`ai` `video` `generation` `text-to-video` `image-to-video` `animation` `cinematic` `wan` `kling` `veo` `hailuo` `sora` `pixverse` `vidu` `ima-api` `content-creation` `video-production` `social-media` `marketing` `tiktok` `reels` `youtube-shorts` `b-roll` `motion-graphics`

---

### 📦 What's Included

- ✅ Complete SKILL.md documentation with examples
- ✅ Production-ready Python script (`ima_video_create.py`)
- ✅ Model capability matrix and cost breakdown
- ✅ Error handling and troubleshooting guide
- ✅ User preference memory system
- ✅ Real-time progress tracking
- ✅ Automatic image upload to OSS
- ✅ Virtual parameter resolution (follows frontend logic)

---

### 🔗 Related Skills

- **ima-image-ai**: AI image generation (text-to-image, image-to-image, upscale, expand)
- **ima-voice-ai**: AI music generation (text-to-music, background music, vocal songs)
- **ima-all-ai**: All-in-one skill for image + video + music workflows

---

### 📄 License & Support

- **License**: MIT (see skill repository)
- **Support**: Issues via GitLab or IMA technical support
- **API Provider**: IMA Studio (https://api.imastudio.com)

---

## Future Roadmap

- [ ] Support for new AI video models as they release
- [ ] Video merging and concatenation
- [ ] Audio track integration with ima-voice-ai
- [ ] Batch generation for multiple clips
- [ ] Video editing presets (transitions, effects)
- [ ] Advanced camera control parameters

---

## Version History

### v1.0.1 (2026-02-27)
- ✅ Initial release with 4 video generation modes
- ✅ 14 models for text_to_video and image_to_video
- ✅ 10 models for first_last_frame_to_video
- ✅ 9 models for reference_image_to_video
- ✅ Automatic image upload via OSS
- ✅ User preference memory
- ✅ Smart credit_rule selection
- ✅ Comprehensive error handling
- ✅ Production-validated on IMA Open API
