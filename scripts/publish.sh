#!/usr/bin/env bash
#
# WisdomCompiler Publish Pipeline
# Single command to prepare, build, and deploy the site.
#
# Usage:
#   ./scripts/publish.sh          # Full pipeline: prepare + build + deploy
#   ./scripts/publish.sh --dry    # Prepare + build only (no deploy)
#   ./scripts/publish.sh --check  # Prepare only (no build, no deploy)
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

DRY_RUN=false
CHECK_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --dry)  DRY_RUN=true ;;
    --check) CHECK_ONLY=true ;;
  esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

step() { echo -e "\n${BLUE}▶ $1${NC}"; }
ok()   { echo -e "  ${GREEN}✓ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠ $1${NC}"; }
fail() { echo -e "  ${RED}✗ $1${NC}"; }

echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  WisdomCompiler Publish Pipeline${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"

ERRORS=0

# ─────────────────────────────────────
# STEP 1: Pre-flight checks
# ─────────────────────────────────────
step "Pre-flight checks"

# Check we're on the right branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "v4" ]]; then
  fail "Not on v4 branch (on: $BRANCH)"
  ERRORS=$((ERRORS + 1))
else
  ok "On branch v4"
fi

# Check for uncommitted changes (warn only)
if ! git diff --quiet HEAD 2>/dev/null; then
  warn "Uncommitted changes detected (will deploy with --commit-dirty)"
fi

# Check tools available
command -v python >/dev/null 2>&1 && ok "Python available" || { fail "Python not found"; ERRORS=$((ERRORS + 1)); }
command -v npx >/dev/null 2>&1 && ok "npx available" || { fail "npx not found"; ERRORS=$((ERRORS + 1)); }

# ─────────────────────────────────────
# STEP 2: Content preparation scripts
# ─────────────────────────────────────
step "Generating book & teacher passage links"
python scripts/generate-book-links.py 2>&1 | tail -5
ok "Book/teacher links generated"

step "Generating random quotes data"
python scripts/generate-quotes.py 2>&1
ok "Random quotes updated (randomquote.inline.ts)"

# ─────────────────────────────────────
# STEP 3: Safety checks
# ─────────────────────────────────────
step "Running safety checks"

# Check Books/index.md is not drafted
if grep -q "draft: true" content/Books/index.md 2>/dev/null; then
  warn "Books/index.md is draft:true — fixing"
  sed -i 's/draft: true/draft: false/' content/Books/index.md
fi
ok "Books/index.md is published"

# Count visible content
BOOK_COUNT=$(grep -rl "draft: false" content/Books/*.md 2>/dev/null | grep -v "_book" | grep -v "index" | wc -l)
TEACHER_COUNT=$(grep -rl "draft: false" content/Teachers/*.md 2>/dev/null | grep -v "_teacher" | grep -v "images" | wc -l)
QUOTE_COUNT=$(grep -rl "Edited: true" "content/Wisdom Quotes/"*.md 2>/dev/null | wc -l)

echo -e "  📊 Content: ${GREEN}$BOOK_COUNT books${NC} | ${GREEN}$TEACHER_COUNT teachers${NC} | ${GREEN}$QUOTE_COUNT quotes${NC}"

# Sanity: at least 30 books and 10 teachers should be visible
if [[ "$BOOK_COUNT" -lt 30 ]]; then
  fail "Only $BOOK_COUNT books visible (expected 30+). Script may have over-drafted."
  ERRORS=$((ERRORS + 1))
fi
if [[ "$TEACHER_COUNT" -lt 10 ]]; then
  fail "Only $TEACHER_COUNT teachers visible (expected 10+). Script may have over-drafted."
  ERRORS=$((ERRORS + 1))
fi

# Check no "No passages collected yet" on un-drafted teacher pages
BAD_TEACHERS=$(grep -rl "draft: false" content/Teachers/*.md 2>/dev/null | xargs grep -l "No passages collected yet" 2>/dev/null | wc -l || true)
BAD_TEACHERS=${BAD_TEACHERS:-0}
BAD_TEACHERS=$(echo "$BAD_TEACHERS" | tr -d '[:space:]')
if [[ "$BAD_TEACHERS" -gt 0 ]]; then
  warn "$BAD_TEACHERS published teacher page(s) still have placeholder text"
fi

if [[ "$ERRORS" -gt 0 ]]; then
  fail "Pre-flight failed with $ERRORS error(s). Fix issues above before publishing."
  exit 1
fi
ok "All safety checks passed"

if $CHECK_ONLY; then
  echo -e "\n${GREEN}Check complete. No build or deploy performed.${NC}"
  exit 0
fi

# ─────────────────────────────────────
# STEP 4: Build
# ─────────────────────────────────────
step "Building site with Quartz"

# Clean stale public directory (Windows NTFS needs special handling)
if [[ -d public ]]; then
  # Use cmd.exe rmdir which handles Windows directory locks properly
  cmd.exe /c "rmdir /s /q public" 2>/dev/null || rm -rf public 2>/dev/null || true
fi

npx quartz build 2>&1 | tail -3
BUILD_EXIT=$?
if [[ "$BUILD_EXIT" -ne 0 ]]; then
  fail "Quartz build failed (exit code $BUILD_EXIT)"
  exit 1
fi
ok "Build succeeded"

FILE_COUNT=$(find public -name "*.html" 2>/dev/null | wc -l)
echo -e "  📄 Emitted ${GREEN}$FILE_COUNT HTML files${NC}"

if $DRY_RUN; then
  echo -e "\n${GREEN}Dry run complete. Site built at public/. No deploy.${NC}"
  echo -e "Preview: ${YELLOW}npx quartz build --serve${NC}"
  exit 0
fi

# ─────────────────────────────────────
# STEP 5: Deploy
# ─────────────────────────────────────
step "Deploying to Cloudflare Pages"

# Clear any conflicting auth tokens
unset CF_API_TOKEN 2>/dev/null || true
unset CLOUDFLARE_API_TOKEN 2>/dev/null || true

npx wrangler pages deploy public \
  --project-name=wisdom-compiler \
  --commit-dirty=true \
  --branch=v4 \
  2>&1 | tail -5

ok "Deployed to Cloudflare Pages"

echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Published successfully!${NC}"
echo -e "${GREEN}  🌐 https://wisdomcompiler.com${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
