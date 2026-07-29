# HomeLab OS Plugins

This directory holds the platform plugins categorized by their primary domain. Each plugin should provide a manifest file defining metadata, versions, permissions, and dependencies, plus python service components and/or static assets for frontend extensions.

## Plugin Categories

- `backup/`: Backups, snapshots, recovery agents.
- `docker/`: Custom container management, template configurations.
- `github/`: Git operations, repository hooks.
- `gitea/`: Private code hosting, webhooks.
- `immich/`: Photo backup integration.
- `jellyfin/`: Media orchestration.
- `media/`: General entertainment/downloads helpers.
- `network/`: DNS, routing, VPN endpoints.
- `custom/`: Local developer modules.
