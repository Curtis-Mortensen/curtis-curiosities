import React from 'react';
import Document, { Html, Head, Main, NextScript, DocumentContext } from 'next/document';

class MyDocument extends Document {
  static async getInitialProps(ctx: DocumentContext) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  render() {
    return (
      <Html lang="en">
        <Head>
          {/* Favicon */}
          <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
          <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
          <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
          <link rel="manifest" href="/site.webmanifest" />
          <meta name="theme-color" content="#ffffff" />
          
          {/* Fonts */}
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
          <link 
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@500;600;700&display=swap" 
            rel="stylesheet"
          />
          
          {/* SEO */}
          <meta name="description" content="Throwing Starfish Studios - Marketing Agency and Game Studio" />
          <meta property="og:title" content="Throwing Starfish Studios" />
          <meta property="og:description" content="Throwing Starfish Studios - Marketing Agency and Game Studio" />
          <meta property="og:type" content="website" />
          <meta property="og:url" content="https://throwingstarfish.com" />
          <meta property="og:image" content="https://throwingstarfish.com/og-image.jpg" />
          <meta name="twitter:card" content="summary_large_image" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument; 