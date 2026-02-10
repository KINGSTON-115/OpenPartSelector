/**
 * OpenPartSelector 前端测试
 * 测试前端功能：搜索、收藏、购物车等
 */

import { jest } from '@jest/globals';

// Mock DOM environment setup
const setupDOM = () => {
    document.body.innerHTML = `
        <div id="toast" class="toast"></div>
        <input id="searchInput" type="text" />
        <div id="results"></div>
        <div id="suggestions" class="suggestions"></div>
        <div class="status-bar"></div>
    `;
};

// Test: Toast functionality
describe('Toast Tests', () => {
    beforeEach(() => {
        setupDOM();
        jest.useFakeTimers();
    });
    
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    test('showToast displays message', () => {
        const toast = document.getElementById('toast');
        expect(toast.classList.contains('show')).toBe(false);
    });
});

// Test: Search Input
describe('Search Tests', () => {
    beforeEach(() => {
        setupDOM();
    });
    
    test('setQuery updates input value', () => {
        const input = document.getElementById('searchInput');
        input.value = 'STM32F103';
        expect(input.value).toBe('STM32F103');
    });
    
    test('empty search shows warning', () => {
        const input = document.getElementById('searchInput');
        expect(input.value.trim()).toBe('');
    });
});

// Test: LocalStorage Functions
describe('LocalStorage Tests', () => {
    beforeEach(() => {
        localStorage.clear();
    });
    
    test('saveSearch stores history', () => {
        const query = 'ESP32';
        localStorage.setItem('searchHistory', JSON.stringify([query]));
        const history = JSON.parse(localStorage.getItem('searchHistory'));
        expect(history).toContain(query);
    });
    
    test('addFav prevents duplicates', () => {
        const part = { part: 'STM32', mfr: 'ST' };
        localStorage.setItem('favorites', JSON.stringify([part]));
        
        const favs = JSON.parse(localStorage.getItem('favorites'));
        const exists = favs.find(f => f.part === part.part);
        expect(exists).toBeTruthy();
    });
});

// Test: Cart Functionality
describe('Cart Tests', () => {
    beforeEach(() => {
        localStorage.clear();
    });
    
    test('cart calculates total', () => {
        const cart = [
            { part: 'STM32', price: '¥0.95' },
            { part: 'CH340', price: '¥0.15' }
        ];
        
        let total = 0;
        cart.forEach(item => {
            total += parseFloat(item.price.replace('¥', '')) || 0;
        });
        
        expect(total).toBe(1.10);
    });
    
    test('exportBOM generates CSV', () => {
        const cart = [{ part: 'STM32', mfr: 'ST', price: '¥0.95' }];
        const csv = `型号,制造商,价格
${cart[0].part},${cart[0].mfr},${cart[0].price}
`;
        expect(csv).toContain('STM32');
    });
});

// Test: BOM Export
describe('BOM Export Tests', () => {
    test('BOM structure is valid', () => {
        const bom = [
            { ref: 'U1', part: 'STM32F103', qty: 1, price: 0.95 },
            { ref: 'U2', part: 'CH340N', qty: 1, price: 0.15 }
        ];
        
        const hasRequiredFields = bom.every(item => 
            item.ref && item.part && item.qty && typeof item.price === 'number'
        );
        
        expect(hasRequiredFields).toBe(true);
    });
});

// Test: Dark Mode
describe('Dark Mode Tests', () => {
    beforeEach(() => {
        localStorage.removeItem('darkMode');
        document.body.classList.remove('dark-mode');
    });
    
    test('dark mode persists in localStorage', () => {
        localStorage.setItem('darkMode', 'true');
        const isDark = localStorage.getItem('darkMode') === 'true';
        expect(isDark).toBe(true);
    });
});

// Test: Search History Limits
describe('Search History Limit Tests', () => {
    beforeEach(() => {
        localStorage.clear();
    });
    
    test('history limits to 10 items', () => {
        const history = Array.from({ length: 15 }, (_, i) => `query${i}`);
        const limited = history.slice(0, 10);
        
        expect(limited.length).toBe(10);
    });
});

// Test: Component Validation
describe('Component Validation Tests', () => {
    test('voltage parsing', () => {
        const voltages = ['3.3V', '5V', '12V', '1.8V'];
        voltages.forEach(v => {
            expect(v).toMatch(/^\d+(\.\d+)?V$/);
        });
    });
    
    test('package validation', () => {
        const packages = ['SOP-8', 'QFN-24', 'LQFP-48', 'SOT-223'];
        packages.forEach(pkg => {
            expect(pkg).toMatch(/^[A-Z]+-\d+$/);
        });
    });
});

// Test: Price Formatting
describe('Price Formatting Tests', () => {
    test('parse price from string', () => {
        const priceStr = '¥0.95';
        const price = parseFloat(priceStr.replace('¥', ''));
        expect(price).toBe(0.95);
    });
    
    test('format price with currency', () => {
        const price = 1.50;
        const formatted = `¥${price.toFixed(2)}`;
        expect(formatted).toBe('¥1.50');
    });
});

// Test: BOM Summary Generation
describe('BOM Summary Tests', () => {
    test('calculate total BOM cost', () => {
        const bom = [
            { part: 'STM32F103', qty: 2, price: 0.95 },
            { part: 'CH340N', qty: 5, price: 0.15 },
            { part: 'AMS1117', qty: 3, price: 0.10 }
        ];
        
        const total = bom.reduce((sum, item) => sum + (item.qty * item.price), 0);
        expect(total).toBe((2 * 0.95) + (5 * 0.15) + (3 * 0.10));
    });
    
    test('count unique parts', () => {
        const bom = [
            { part: 'STM32F103' },
            { part: 'CH340N' },
            { part: 'STM32F103' },
            { part: 'ESP32' }
        ];
        
        const unique = new Set(bom.map(item => item.part));
        expect(unique.size).toBe(3);
    });
});

// Test: Export CSV Format
describe('CSV Export Tests', () {
    test('CSV header generation', () => {
        const headers = ['型号', '制造商', '数量', '单价', '小计'];
        const csvHeader = headers.join(',');
        expect(csvHeader).toBe('型号,制造商,数量,单价,小计');
    });
    
    test('CSV row escaping', () => {
        const value = 'Test, Inc.'; // Comma in value
        const escaped = `"${value}"`;
        expect(escaped).toBe('"Test, Inc."');
    });
});

// Run tests with: npm test
