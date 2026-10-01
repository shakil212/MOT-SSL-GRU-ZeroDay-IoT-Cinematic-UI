# Model artifacts

Store verified exports locally under `artifacts/<bundle-id>/`. Bundle contents are ignored by Git. Never overwrite a verified bundle; assign a new identifier for a new export.

Each future bundle must include a `manifest.json` recording notebook revision, export date, framework versions, file checksums, confirmed input/output specifications, and the associated LOAFO experiment/fold. Include preprocessing objects, class mappings, or thresholds only if the actual training pipeline uses them.

No format, framework, or model file is assumed yet. Record the approved external storage location and retrieval instructions here when available. They have not been chosen yet. Keep binaries outside ordinary Git; evaluate external storage or Git LFS when exports exist.
