import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useAuthStore } from '@/store';

/**
 * Écran de profil utilisateur
 */
export default function ProfileScreen() {
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    Alert.alert(
      'Déconnexion',
      'Êtes-vous sûr de vouloir vous déconnecter ?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Déconnexion',
          style: 'destructive',
          onPress: () => {
            logout();
            router.replace('/(auth)/login');
          },
        },
      ]
    );
  };

  const menuItems = [
    { icon: 'settings-outline', label: 'Paramètres', route: '/settings' },
    { icon: 'document-text-outline', label: 'Documentation', route: '/docs' },
    { icon: 'information-circle-outline', label: 'À propos', route: '/about' },
    { icon: 'help-circle-outline', label: 'Aide', route: '/help' },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* En-tête profil */}
      <View style={styles.profileHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.name?.charAt(0).toUpperCase() || 'G'}
          </Text>
        </View>
        <Text style={styles.userName}>{user?.name || 'Gestionnaire'}</Text>
        <Text style={styles.userEmail}>{user?.email || 'email@exemple.com'}</Text>
        <View style={styles.roleBadge}>
          <Text style={styles.roleText}>
            {user?.role === 'portfolio_manager' ? 'Gestionnaire de Portefeuille' : 'Utilisateur'}
          </Text>
        </View>
      </View>

      {/* Préférences */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Préférences</Text>
        
        <View style={styles.prefItem}>
          <Text style={styles.prefLabel}>Taux sans risque par défaut</Text>
          <Text style={styles.prefValue}>
            {((user?.preferences?.defaultRiskFreeRate || 0.02) * 100).toFixed(1)}%
          </Text>
        </View>

        <View style={styles.prefItem}>
          <Text style={styles.prefLabel}>Devise</Text>
          <Text style={styles.prefValue}>
            {user?.preferences?.defaultCurrency || 'EUR'}
          </Text>
        </View>

        <View style={styles.prefItem}>
          <Text style={styles.prefLabel}>Thème</Text>
          <Text style={styles.prefValue}>
            {user?.preferences?.theme === 'dark' ? 'Sombre' : 'Clair'}
          </Text>
        </View>
      </View>

      {/* Menu */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Menu</Text>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.menuItem}
            onPress={() => {/* Navigation */}}
          >
            <Ionicons name={item.icon as any} size={22} color="#8892b0" />
            <Text style={styles.menuLabel}>{item.label}</Text>
            <Ionicons name="chevron-forward" size={20} color="#5a6785" />
          </TouchableOpacity>
        ))}
      </View>

      {/* Informations sur le modèle */}
      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Modèle Mathématique</Text>
        <Text style={styles.infoText}>
          Cette application utilise le modèle de Markowitz pour l'optimisation de portefeuille.
          Elle implémente les 14 points du document de référence sur la théorie moderne du portefeuille.
        </Text>
        <View style={styles.mathBox}>
          <Text style={styles.mathFormula}>min w'Σw  s.t.  w'μ ≥ r*</Text>
        </View>
      </View>

      {/* Déconnexion */}
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Ionicons name="log-out-outline" size={20} color="#e94560" />
        <Text style={styles.logoutText}>Se déconnecter</Text>
      </TouchableOpacity>

      {/* Version */}
      <Text style={styles.version}>Portfolio Optimizer v1.0.0</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#16213e',
  },
  profileHeader: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#1a1a2e',
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#e94560',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  userName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#ccd6f6',
  },
  userEmail: {
    fontSize: 14,
    color: '#8892b0',
    marginTop: 4,
  },
  roleBadge: {
    backgroundColor: '#0f3460',
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 20,
    marginTop: 12,
  },
  roleText: {
    color: '#64ffda',
    fontSize: 12,
  },
  section: {
    marginTop: 20,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#e94560',
    marginBottom: 12,
    marginLeft: 4,
  },
  prefItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#1a1a2e',
    padding: 16,
    borderRadius: 8,
    marginBottom: 8,
  },
  prefLabel: {
    color: '#ccd6f6',
  },
  prefValue: {
    color: '#64ffda',
    fontWeight: '600',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1a1a2e',
    padding: 16,
    borderRadius: 8,
    marginBottom: 8,
  },
  menuLabel: {
    color: '#ccd6f6',
    flex: 1,
    marginLeft: 12,
  },
  infoCard: {
    backgroundColor: '#0f3460',
    margin: 16,
    padding: 20,
    borderRadius: 16,
  },
  infoTitle: {
    color: '#ccd6f6',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  infoText: {
    color: '#8892b0',
    fontSize: 13,
    lineHeight: 20,
  },
  mathBox: {
    backgroundColor: '#1a1a2e',
    padding: 12,
    borderRadius: 8,
    marginTop: 12,
    alignItems: 'center',
  },
  mathFormula: {
    color: '#64ffda',
    fontFamily: 'monospace',
    fontSize: 14,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    margin: 16,
    padding: 16,
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e94560',
  },
  logoutText: {
    color: '#e94560',
    marginLeft: 8,
    fontWeight: '600',
  },
  version: {
    textAlign: 'center',
    color: '#5a6785',
    fontSize: 12,
    marginBottom: 40,
  },
});
