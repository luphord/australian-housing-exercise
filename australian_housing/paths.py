from pathlib import Path

try:
    project_dir = Path(__file__).resolve().parents[1]
except:
    project_dir = Path('.')

class _PathManager:
    @property
    def project_dir(self):
        return project_dir

    @property
    def raw_data_file(self):
        return self.project_dir / 'data' / 'raw' / 'australian_housing.json'

    @property
    def interim_data_file(self):
        return self.project_dir / 'data' / 'interim' / 'australian_housing_decoded.csv'

    @property
    def processed_data_file(self):
        return self.project_dir / 'data' / 'processed' / 'new_south_wales_housing.csv'

manager = _PathManager()
