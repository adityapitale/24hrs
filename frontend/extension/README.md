# Chrome Extension

The PhishGuard Chrome extension augments the Gmail web interface with risk insights, color-coded badges, and on-demand sandbox triggers.

## Planned Features

- Manifest V3 service worker and content scripts
- Gmail DOM augmentation with overlays and tooltips
- WebSocket subscription to alerting service
- Context menu integration for sandboxing links
- Local storage for user preferences and acknowledgement history

## Setup (planned)

1. Install dependencies with `pnpm install`.
2. Build the extension using `pnpm run build`.
3. Load the `dist` directory as an unpacked extension in Chrome for development.

Detailed implementation will be added in subsequent milestones.

