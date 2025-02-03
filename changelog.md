# Changelog

## [2.1.0] - 2024-02-02
### Added
- LAN IP detection for server registration
- Client-side registry IP configuration
- Wireless network support
- Firewall setup documentation
- updated file organization

### Changed
- Server registration uses actual LAN IP instead of localhost
- Improved connection error messages
- Updated UI for better network status visibility

### Fixed
- Server list refresh issues
- Certificate validation edge cases
- Message encryption thread safety

## [2.0.0] - 2024-01-06
### Added
- SSL/TLS encryption layer
- Certificate-based authentication
- Matrix-style UI theme
- Server browser interface

### Changed
- Upgraded to Fernet 41.0+ encryption
- Revised protocol handshake sequence