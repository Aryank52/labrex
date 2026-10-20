import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LABREX — Labour Market Intelligence & Policy Optimization",
  description: "AI-Powered Labour Market Intelligence, Workforce Forecasting, Skill-Gap Intelligence & Policy Optimization Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0B0F17] text-[#F9FAFB] antialiased">
        {children}
      </body>
    </html>
  );
}
