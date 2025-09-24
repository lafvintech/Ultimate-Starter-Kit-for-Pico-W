#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fake PNG Converter Script

This script processes fake PNG files identified in the CSV report,
converts them to proper PNG format, and replaces the original files.
"""

import os
import csv
import shutil
from datetime import datetime
from PIL import Image
import json

def create_output_directory(base_path):
    """Create the converted_pngs output directory"""
    output_dir = os.path.join(base_path, "converted_pngs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    return output_dir

def parse_csv_report(csv_file_path):
    """Parse the CSV report and extract fake PNG file information"""
    fake_pngs = []
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(csv_file_path, 'r', encoding=encoding) as csvfile:
                    reader = csv.DictReader(csvfile)
                    fake_pngs = []
                    
                    for row in reader:
                        if row['IsFakePng'].lower() == 'true':
                            fake_pngs.append({
                                'filename': row['FileName'],
                                'filepath': row['FilePath'],
                                'actual_format': row['ActualFormat'],
                                'filesize': row['FileSize']
                            })
                    
                    print(f"Successfully parsed CSV with {encoding} encoding")
                    print(f"Found {len(fake_pngs)} fake PNG files to convert")
                    return fake_pngs
                    
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error with {encoding} encoding: {e}")
                continue
        
        print("Failed to parse CSV with any encoding")
        return []
    
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return []

def convert_image_to_png(source_path, output_dir, filename):
    """Convert an image file to PNG format"""
    try:
        # Open the image
        with Image.open(source_path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Keep transparency for formats that support it
                if img.mode == 'P' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                elif img.mode == 'LA':
                    img = img.convert('RGBA')
            elif img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Create output path
            output_path = os.path.join(output_dir, filename)
            
            # Save as PNG with high quality
            img.save(output_path, 'PNG', optimize=False, compress_level=1)
            
            return {
                'success': True,
                'output_path': output_path,
                'message': f"Successfully converted {filename}"
            }
    
    except Exception as e:
        return {
            'success': False,
            'output_path': None,
            'message': f"Failed to convert {filename}: {str(e)}"
        }

def replace_original_file(original_path, converted_path):
    """Replace the original fake PNG with the converted PNG"""
    try:
        # Create backup of original file
        backup_path = original_path + '.backup'
        shutil.copy2(original_path, backup_path)
        
        # Replace original with converted file
        shutil.copy2(converted_path, original_path)
        
        return {
            'success': True,
            'backup_path': backup_path,
            'message': f"Successfully replaced {os.path.basename(original_path)}"
        }
    
    except Exception as e:
        return {
            'success': False,
            'backup_path': None,
            'message': f"Failed to replace {os.path.basename(original_path)}: {str(e)}"
        }

def generate_report(conversion_results, replacement_results, output_dir):
    """Generate detailed execution report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_files_processed': len(conversion_results),
            'successful_conversions': sum(1 for r in conversion_results if r['conversion']['success']),
            'failed_conversions': sum(1 for r in conversion_results if not r['conversion']['success']),
            'successful_replacements': sum(1 for r in replacement_results if r['success']),
            'failed_replacements': sum(1 for r in replacement_results if not r['success'])
        },
        'conversion_details': conversion_results,
        'replacement_details': replacement_results
    }
    
    # Save JSON report
    report_path = os.path.join(output_dir, 'conversion_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Save human-readable report
    txt_report_path = os.path.join(output_dir, 'conversion_report.txt')
    with open(txt_report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("FAKE PNG CONVERSION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {report['timestamp']}\n\n")
        
        f.write("SUMMARY:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total files processed: {report['summary']['total_files_processed']}\n")
        f.write(f"Successful conversions: {report['summary']['successful_conversions']}\n")
        f.write(f"Failed conversions: {report['summary']['failed_conversions']}\n")
        f.write(f"Successful replacements: {report['summary']['successful_replacements']}\n")
        f.write(f"Failed replacements: {report['summary']['failed_replacements']}\n\n")
        
        f.write("CONVERSION DETAILS:\n")
        f.write("-" * 30 + "\n")
        for result in conversion_results:
            status = "✓" if result['conversion']['success'] else "✗"
            f.write(f"{status} {result['filename']} ({result['actual_format']})\n")
            f.write(f"   Original: {result['original_path']}\n")
            if result['conversion']['success']:
                f.write(f"   Converted: {result['conversion']['output_path']}\n")
            f.write(f"   Message: {result['conversion']['message']}\n\n")
        
        f.write("REPLACEMENT DETAILS:\n")
        f.write("-" * 30 + "\n")
        for result in replacement_results:
            status = "✓" if result['success'] else "✗"
            f.write(f"{status} {result['message']}\n")
            if result['success'] and result['backup_path']:
                f.write(f"   Backup created: {result['backup_path']}\n")
            f.write("\n")
    
    print(f"\nDetailed reports saved:")
    print(f"  JSON: {report_path}")
    print(f"  Text: {txt_report_path}")
    
    return report

def main():
    """Main execution function"""
    # Configuration
    base_path = r"i:\Github\Ultimate-_tarter_Kit_for_Pico_W_PDF\Ultimate-Starter-Kit-for-Pico-W"
    csv_file_path = os.path.join(base_path, "fake_png_report.csv")
    
    print("Starting Fake PNG Conversion Process...")
    print("=" * 50)
    
    # Step 1: Create output directory
    output_dir = create_output_directory(base_path)
    
    # Step 2: Parse CSV report
    fake_pngs = parse_csv_report(csv_file_path)
    if not fake_pngs:
        print("No fake PNG files found or error parsing CSV.")
        return
    
    # Step 3: Convert fake PNGs to proper PNG format
    print("\nStep 1: Converting fake PNG files...")
    conversion_results = []
    
    for fake_png in fake_pngs:
        print(f"Processing: {fake_png['filename']} ({fake_png['actual_format']})")
        
        conversion_result = convert_image_to_png(
            fake_png['filepath'],
            output_dir,
            fake_png['filename']
        )
        
        result_entry = {
            'filename': fake_png['filename'],
            'original_path': fake_png['filepath'],
            'actual_format': fake_png['actual_format'],
            'conversion': conversion_result
        }
        
        conversion_results.append(result_entry)
        
        if conversion_result['success']:
            print(f"  ✓ {conversion_result['message']}")
        else:
            print(f"  ✗ {conversion_result['message']}")
    
    # Step 4: Replace original files with converted ones
    print("\nStep 2: Replacing original files...")
    replacement_results = []
    
    for result in conversion_results:
        if result['conversion']['success']:
            replacement_result = replace_original_file(
                result['original_path'],
                result['conversion']['output_path']
            )
            replacement_results.append(replacement_result)
            
            if replacement_result['success']:
                print(f"  ✓ {replacement_result['message']}")
            else:
                print(f"  ✗ {replacement_result['message']}")
        else:
            replacement_results.append({
                'success': False,
                'backup_path': None,
                'message': f"Skipped replacement for {result['filename']} (conversion failed)"
            })
            print(f"  - Skipped {result['filename']} (conversion failed)")
    
    # Step 5: Generate detailed report
    print("\nStep 3: Generating execution report...")
    report = generate_report(conversion_results, replacement_results, output_dir)
    
    # Final summary
    print("\n" + "=" * 50)
    print("CONVERSION PROCESS COMPLETED")
    print("=" * 50)
    print(f"Total files processed: {report['summary']['total_files_processed']}")
    print(f"Successful conversions: {report['summary']['successful_conversions']}")
    print(f"Failed conversions: {report['summary']['failed_conversions']}")
    print(f"Successful replacements: {report['summary']['successful_replacements']}")
    print(f"Failed replacements: {report['summary']['failed_replacements']}")
    
    if report['summary']['failed_conversions'] > 0 or report['summary']['failed_replacements'] > 0:
        print("\n⚠️  Some operations failed. Check the detailed report for more information.")
    else:
        print("\n✅ All operations completed successfully!")

if __name__ == "__main__":
    main()