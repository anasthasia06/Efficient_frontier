import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import { router } from 'expo-router';
import { useAuthStore } from '@/store';

/**
 * Écran de connexion pour les gestionnaires de portefeuille
 */
export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const { login, isLoading, setLoading } = useAuthStore();

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Veuillez remplir tous les champs');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Simulation d'appel API - À remplacer par vrai appel
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Login simulé pour démo
      if (email === 'demo@portfolio.com' && password === 'demo123') {
        login(
          {
            id: '1',
            email,
            name: 'Gestionnaire Demo',
            role: 'portfolio_manager',
            preferences: {
              defaultRiskFreeRate: 0.02,
              defaultCurrency: 'EUR',
              theme: 'dark',
            },
          },
          'demo-token-123'
        );
        router.replace('/(tabs)');
      } else {
        setError('Identifiants incorrects');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <View style={styles.header}>
        <Text style={styles.title}>Portfolio Optimizer</Text>
        <Text style={styles.subtitle}>Optimisation de Portefeuille - Markowitz</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          placeholder="email@exemple.com"
          placeholderTextColor="#666"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />

        <Text style={styles.label}>Mot de passe</Text>
        <TextInput
          style={styles.input}
          placeholder="••••••••"
          placeholderTextColor="#666"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        {error ? <Text style={styles.error}>{error}</Text> : null}

        <TouchableOpacity
          style={[styles.button, isLoading && styles.buttonDisabled]}
          onPress={handleLogin}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Se connecter</Text>
          )}
        </TouchableOpacity>

        <View style={styles.demoInfo}>
          <Text style={styles.demoText}>Compte de démonstration :</Text>
          <Text style={styles.demoCredentials}>demo@portfolio.com / demo123</Text>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#16213e',
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#e94560',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#8892b0',
  },
  form: {
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    padding: 24,
  },
  label: {
    color: '#ccd6f6',
    fontSize: 14,
    marginBottom: 8,
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#0f0f23',
    borderRadius: 8,
    padding: 16,
    color: '#fff',
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#2d3a5a',
  },
  button: {
    backgroundColor: '#e94560',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  error: {
    color: '#ff6b6b',
    textAlign: 'center',
    marginBottom: 16,
  },
  demoInfo: {
    marginTop: 24,
    alignItems: 'center',
  },
  demoText: {
    color: '#8892b0',
    fontSize: 12,
  },
  demoCredentials: {
    color: '#64ffda',
    fontSize: 12,
    marginTop: 4,
  },
});
