/**
 * Frontend Tests for OpenPartSelector
 * v1.1.32
 */

const fs = require('fs');
const path = require('path');

// Test utilities
describe('OpenPartSelector Frontend', () => {
    
    describe('HTML Structure', () => {
        let html;
        
        beforeAll(() => {
            html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
        });
        
        test('index.html exists and is readable', () => {
            expect(html).toBeTruthy();
            expect(html.length).toBeGreaterThan(1000);
        });
        
        test('contains version info', () => {
            expect(html).toContain('v1.1.32');
            expect(html).toContain('OpenPartSelector');
        });
        
        test('has proper meta tags', () => {
            expect(html).toContain('<!DOCTYPE html>');
            expect(html).toContain('<meta charset="UTF-8">');
        });
        
        test('contains title', () => {
            expect(html).toContain('<title>');
            expect(html).toContain('OpenPartSelector');
        });
    });
    
    describe('UI Components', () => {
        let html;
        
        beforeAll(() => {
            html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
        });
        
        test('has search functionality', () => {
            expect(html).toContain('search');
            expect(html).toContain('input');
        });
        
        test('has component database indicator', () => {
            expect(html).toContain('48+');
        });
        
        test('has version markers in code', () => {
            // Check for version strings in comments
            expect(html).toContain('v1.1.32');
        });
    });
    
    describe('Feature Flags', () => {
        let html;
        
        beforeAll(() => {
            html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
        });
        
        test('has calculator features', () => {
            expect(html).toContain('calculator');
        });
        
        test('has database features', () => {
            expect(html).toContain('database');
        });
    });
});

// Test runner
if (require.main === module) {
    const Jest = require('jest');
    const config = {
        testEnvironment: 'node',
        testMatch: ['**/__tests__/**/*.test.js'],
        verbose: true
    };
    Jest.run(['--config', JSON.stringify(config)]);
}
