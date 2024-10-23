import Navbar from "@/components/Navbar";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthenticationContext";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="fr">
      <body>
        <AuthProvider>
          <div className="h-[90vh]">
            <div className="fond"></div>
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
