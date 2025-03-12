const { test, expect } = require('@playwright/test');

test('sanity check', async ({ page }) => {
  // Go to the starting URL
  await page.goto('http://localhost:3000');

  // Check that the title is correct
  await expect(page).toHaveTitle(/bleedy.py/);

  // Check that the logo is visible
  const logo = await page.$('.logo');
  expect(logo).toBeVisible();

  // Check that the header text is correct
  const headerText = await page.textContent('.app-name');
  expect(headerText).toBe('bleedy.py');

  // Check that the footer text is correct
  const footerText = await page.textContent('.footer-content');
  expect(footerText).toContain('Based on bleedy.py, by North101 and OliviaJuliet.');
  expect(footerText).toContain('Created by Buteremelse.');
  expect(footerText).toContain('This website is not produced, endorsed, supported, or affiliated with Fantasy Flight Games.');
});
