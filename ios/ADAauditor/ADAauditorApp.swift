import SwiftUI

@main
struct ADAauditorApp: App {

    // MARK: - Design tokens (Sovereign Auditor palette)
    static let primaryColor   = Color(hex: 0x0C1427)
    static let backgroundColor = Color(hex: 0xF7F9FB)
    static let errorColor     = Color(hex: 0xBA1A1A)

    @State private var showSplash = true

    var body: some Scene {
        WindowGroup {
            ZStack {
                ContentView()
                    .opacity(showSplash ? 0 : 1)

                if showSplash {
                    SplashView()
                        .transition(.opacity)
                }
            }
            .onAppear {
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.8) {
                    withAnimation(.easeOut(duration: 0.4)) {
                        showSplash = false
                    }
                }
            }
        }
    }
}

// MARK: - Content View (hosts the WebView full-screen)

struct ContentView: View {
    var body: some View {
        EnhancedWebView(
            url: URL(string: "https://ada-auditor-908021165922.us-central1.run.app")!
        )
        .ignoresSafeArea()
        .tint(ADAauditorApp.primaryColor)
    }
}

// MARK: - Splash / Launch Screen

struct SplashView: View {
    var body: some View {
        ZStack {
            ADAauditorApp.backgroundColor
                .ignoresSafeArea()

            VStack(spacing: 20) {
                // App icon placeholder
                ZStack {
                    RoundedRectangle(cornerRadius: 24, style: .continuous)
                        .fill(ADAauditorApp.primaryColor)
                        .frame(width: 100, height: 100)

                    Image(systemName: "building.2.fill")
                        .font(.system(size: 44))
                        .foregroundColor(.white)
                }

                Text("ADA Auditor")
                    .font(.system(size: 28, weight: .bold, design: .default))
                    .foregroundColor(ADAauditorApp.primaryColor)

                Text("Sovereign Auditor")
                    .font(.system(size: 14, weight: .medium, design: .default))
                    .foregroundColor(ADAauditorApp.primaryColor.opacity(0.55))

                ProgressView()
                    .tint(ADAauditorApp.primaryColor)
                    .padding(.top, 16)
            }
        }
    }
}

// MARK: - Color extension for hex literals

extension Color {
    init(hex: UInt, alpha: Double = 1.0) {
        self.init(
            .sRGB,
            red:   Double((hex >> 16) & 0xFF) / 255.0,
            green: Double((hex >> 8)  & 0xFF) / 255.0,
            blue:  Double( hex        & 0xFF) / 255.0,
            opacity: alpha
        )
    }
}
