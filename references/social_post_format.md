# Standard social post format for reasoning-core content (Gene-approved 2026-08-11).
# Format: [attention hook] + [infographic image attached] + [video link] + [GitHub link]
#
# WHY: the previous posts were half-broken (X cut the GH link at 280 chars; LinkedIn
# had GH but no video link). The infographic is the attention-grabber (Studio analytics:
# Browse = 39.5% of views, "high-contrast thumbnails" recommended). The video link gives
# the preview card. The GH link is the credibility anchor.

# === X (280 chars — URLs count as ~23) ===
X_TEMPLATE = """{hook}
{video_url}
{github_url}"""

# Example (fits under 280 with 2 urls):
# hook: "Same data, wildly different reasoning. Why? Epiplexity: measure the shape of reasoning, not the mass of memory."
# video_url: https://youtu.be/uR4RElrx6uI
# github_url: https://github.com/Godsend/reasoning-core
# X counts: ~126 + 23 + 23 = ~172. FITS. (Previous failure: 3 urls + longer text = 284, GH got cut.)

# === LinkedIn (3000 chars — plenty) ===
LINKEDIN_TEMPLATE = """{hook}

{video_url}

{video_desc}

Full paper + framework: {github_url}
Interactive notebook with Consensus citations: {notebook_url}

#EILT #Epiplexity #MachineLearning #AIReasoning"""

# On LinkedIn, attach the infographic PNG (or the video itself — it embeds a preview card).
# Order in composer: type text -> attach image/video -> post.

# === The infographic ===
# Clean title card: media/epiplexity-judge-witness-title-card.png (verified clean).
# Regeneration recipe if a new one is needed:
#   generate_infographic with explicit instructions listing exact words + spellings;
#   vision-verify; regenerate with corrupted words called out. Clean on pass 2.

# === Standard flow (one video) ===
# 1. Upload video to YouTube via youtube_upload_publish_cdp.js (VIDEO_PUBLISH=1)
# 2. Get youtu.be/<id> from the channel videos page
# 3. X: hook + video url + GH url (keep under 280)
# 4. LinkedIn: hook + video url + desc + GH + notebook, attach infographic
# 5. Close tabs after each share (tab hygiene rule)
