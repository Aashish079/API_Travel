const puppeteer = require('puppeteer');

async function automateClaudeContinue() {
  // Launch the browser
  const browser = await puppeteer.launch({
    headless: false, // Set to true if you don't need to see the browser
    defaultViewport: null
  });

  // Create a new page
  const page = await browser.newPage();

  // Navigate to Claude (you'll need to log in manually first time)
  await page.goto('https://claude.ai/chat');

  // Function to check if Claude is still generating
  const isGenerating = async () => {
    try {
      // Look for the "Stop generating" button which appears while Claude is generating
      const stopButton = await page.$('button:has-text("Stop generating")');
      return !stopButton;
    } catch (error) {
      return false;
    }
  };

  // Function to send "Continue" when generation stops
  const sendContinue = async () => {
    try {
      // Wait for the input box to be available
      const inputBox = await page.waitForSelector('textarea[placeholder="Message Claude..."]');
      
      // Type "Continue" in the input box
      await inputBox.type('Continue');
      
      // Press Enter
      await inputBox.press('Enter');
      
      console.log('Sent Continue command');
    } catch (error) {
      console.error('Error sending Continue:', error);
    }
  };

  // Main loop to monitor Claude's state
  while (true) {
    try {
      // Check if Claude has stopped generating
      if (!await isGenerating()) {
        await sendContinue();
      }
      
      // Wait a short time before checking again
      await page.waitForTimeout(2000);
    } catch (error) {
      console.error('Error in main loop:', error);
    }
  }
}

// Run the automation
automateClaudeContinue().catch(console.error);