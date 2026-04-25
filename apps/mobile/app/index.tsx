import { Redirect } from "expo-router";

export default function Index() {
  // Redirige la route racine vers le groupe de tabs
  return <Redirect href="/(tabs)" />;
}
