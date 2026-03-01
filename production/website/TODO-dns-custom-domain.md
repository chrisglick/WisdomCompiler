---
title: "TODO: Complete Custom Domain Setup"
created: 2026-03-01
status: pending
priority: high
---

# Complete wisdomcompiler.com Custom Domain Setup

## What's Done
- [x] Domain registered on Porkbun (wisdomcompiler.com)
- [x] Quartz v4 vault built at D:\Vaults\WisdomCompiler\
- [x] Content migrated (39 books, 2 teachers, 649 wisdom quotes, 654 images)
- [x] Cloudflare Pages project created: `wisdom-compiler`
- [x] Site deployed and live at https://wisdom-compiler.pages.dev
- [x] Domain added to Cloudflare DNS (free zone)
- [x] Porkbun nameservers updated to Cloudflare's nameservers
- [x] Git repo at github.com/chrisglick/WisdomCompiler (branch: v4)

## What's Pending (Do When DNS Propagates)

### 1. Verify domain is active in Cloudflare
- Go to https://dash.cloudflare.com
- Check if wisdomcompiler.com shows **Active** status (green checkmark)
- If still "Pending Nameserver Update" — wait longer (can take up to 48 hours)

### 2. Add custom domain to Pages project
- Go to **Workers & Pages** → **wisdom-compiler** → **Custom domains** tab
- Click **Set up a custom domain**
- Enter: `wisdomcompiler.com`
- Click **Activate domain**
- Cloudflare auto-creates the CNAME record and provisions HTTPS

### 3. Add www subdomain
- Same tab → add `www.wisdomcompiler.com` as another custom domain

### 4. Verify site is live
```bash
curl -sf https://wisdomcompiler.com
curl -sf https://www.wisdomcompiler.com
```

### 5. Test HTTPS
- Visit https://wisdomcompiler.com in browser
- Confirm padlock icon (valid SSL)

## Quick Commands
```bash
# Check DNS propagation
nslookup wisdomcompiler.com 8.8.8.8

# Rebuild and redeploy site
cd D:\Vaults\WisdomCompiler
npx quartz build
npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4

# Local preview
cd D:\Vaults\WisdomCompiler
npx quartz build --serve
# Opens at http://localhost:8080
```

## Current Live URLs
- **Production (pages.dev):** https://wisdom-compiler.pages.dev (LIVE NOW)
- **Custom domain:** https://wisdomcompiler.com (pending DNS propagation)
