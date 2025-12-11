def run(file_path, metadata):
    # example plugin that returns an auto-tag based on filename
    tags = []
    name = file_path.lower()
    if 'invoice' in name:
        tags.append('invoice')
    if '.jpg' in name or '.png' in name:
        tags.append('image')
    if not tags:
        tags.append('unknown')
    return {'tags': tags}
