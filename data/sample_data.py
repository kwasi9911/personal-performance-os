"""Generate a synthetic Apple Health XML for demo purposes."""
import random
from datetime import datetime, timedelta

def generate_sample_xml(output_path='data/sample_export.xml'):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<!DOCTYPE HealthData>',
             '<HealthData locale="en_US">']
    base = datetime(2024, 1, 1)
    for day_offset in range(365):
        date = base + timedelta(days=day_offset)
        ds = date.strftime('%Y-%m-%d %H:%M:%S +0000')
        steps = random.randint(3000, 15000)
        ex = random.randint(0, 60)
        lines.append(f'  <Record type="HKQuantityTypeIdentifierStepCount" value="{steps}" unit="count" startDate="{ds}" endDate="{ds}"/>')
        lines.append(f'  <Record type="HKQuantityTypeIdentifierExerciseTime" value="{ex}" unit="min" startDate="{ds}" endDate="{ds}"/>')
    lines.append('</HealthData>')
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'Sample XML written to {output_path}')

if __name__ == '__main__':
    generate_sample_xml()
