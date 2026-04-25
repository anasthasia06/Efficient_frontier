import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useStrategyStore, useOptimizationStore } from '@/store';
import type { InvestmentStrategy } from '@/types/portfolio';

/**
 * Écran de gestion des stratégies d'investissement
 * Permet de définir et sauvegarder des profils de risque
 */
export default function StrategyScreen() {
  const { strategies, addStrategy, setActiveStrategy, activeStrategy } = useStrategyStore();
  const { setConstraints } = useOptimizationStore();

  const [isCreating, setIsCreating] = useState(false);
  const [newStrategyName, setNewStrategyName] = useState('');
  const [targetReturn, setTargetReturn] = useState('8');
  const [maxVolatility, setMaxVolatility] = useState('15');
  const [riskProfile, setRiskProfile] = useState<'conservative' | 'moderate' | 'aggressive'>('moderate');

  const predefinedStrategies: Partial<InvestmentStrategy>[] = [
    {
      name: 'Prudent',
      description: 'Faible risque, rendement stable',
      riskProfile: 'conservative',
      constraints: {
        targetReturn: 0.04,
        maxVolatility: 0.08,
        minWeight: 0,
        maxWeight: 0.4,
        allowShortSelling: false,
        riskFreeRate: 0.02,
      },
    },
    {
      name: 'Équilibré',
      description: 'Risque modéré, rendement intermédiaire',
      riskProfile: 'moderate',
      constraints: {
        targetReturn: 0.07,
        maxVolatility: 0.12,
        minWeight: 0,
        maxWeight: 0.6,
        allowShortSelling: false,
        riskFreeRate: 0.02,
      },
    },
    {
      name: 'Dynamique',
      description: 'Risque élevé, potentiel de rendement supérieur',
      riskProfile: 'aggressive',
      constraints: {
        targetReturn: 0.12,
        maxVolatility: 0.25,
        minWeight: -0.1,
        maxWeight: 1,
        allowShortSelling: true,
        riskFreeRate: 0.02,
      },
    },
  ];

  const handleSelectStrategy = (strategy: InvestmentStrategy | Partial<InvestmentStrategy>) => {
    if (strategy.constraints) {
      setConstraints(strategy.constraints);
      setActiveStrategy(strategy as InvestmentStrategy);
    }
  };

  const handleCreateStrategy = () => {
    const newStrategy: InvestmentStrategy = {
      id: Date.now().toString(),
      name: newStrategyName || 'Ma stratégie',
      description: `Rendement cible: ${targetReturn}%, Vol max: ${maxVolatility}%`,
      riskProfile,
      constraints: {
        targetReturn: parseFloat(targetReturn) / 100,
        maxVolatility: parseFloat(maxVolatility) / 100,
        minWeight: 0,
        maxWeight: 1,
        allowShortSelling: riskProfile === 'aggressive',
        riskFreeRate: 0.02,
      },
      rebalancingFrequency: 'monthly',
      createdAt: new Date().toISOString(),
    };

    addStrategy(newStrategy);
    setIsCreating(false);
    setNewStrategyName('');
  };

  const getRiskColor = (profile: string) => {
    switch (profile) {
      case 'conservative': return '#64ffda';
      case 'moderate': return '#ffd93d';
      case 'aggressive': return '#e94560';
      default: return '#8892b0';
    }
  };

  const getRiskIcon = (profile: string) => {
    switch (profile) {
      case 'conservative': return 'shield-checkmark';
      case 'moderate': return 'analytics';
      case 'aggressive': return 'rocket';
      default: return 'help-circle';
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Stratégies d'Investissement</Text>
        <Text style={styles.subtitle}>Définissez votre exposition au risque</Text>
      </View>

      {/* Stratégies prédéfinies */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Profils de risque</Text>
        {predefinedStrategies.map((strategy, index) => (
          <TouchableOpacity
            key={index}
            style={[
              styles.strategyCard,
              activeStrategy?.name === strategy.name && styles.activeCard,
            ]}
            onPress={() => handleSelectStrategy(strategy)}
          >
            <View style={styles.strategyHeader}>
              <Ionicons
                name={getRiskIcon(strategy.riskProfile!) as any}
                size={24}
                color={getRiskColor(strategy.riskProfile!)}
              />
              <Text style={styles.strategyName}>{strategy.name}</Text>
            </View>
            <Text style={styles.strategyDescription}>{strategy.description}</Text>
            <View style={styles.strategyDetails}>
              <Text style={styles.detailText}>
                μ: {((strategy.constraints?.targetReturn || 0) * 100).toFixed(0)}%
              </Text>
              <Text style={styles.detailText}>
                σ max: {((strategy.constraints?.maxVolatility || 0) * 100).toFixed(0)}%
              </Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Stratégies personnalisées */}
      {strategies.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Mes stratégies</Text>
          {strategies.map((strategy) => (
            <TouchableOpacity
              key={strategy.id}
              style={[
                styles.strategyCard,
                activeStrategy?.id === strategy.id && styles.activeCard,
              ]}
              onPress={() => handleSelectStrategy(strategy)}
            >
              <View style={styles.strategyHeader}>
                <Ionicons
                  name="bookmark"
                  size={20}
                  color="#e94560"
                />
                <Text style={styles.strategyName}>{strategy.name}</Text>
              </View>
              <Text style={styles.strategyDescription}>{strategy.description}</Text>
            </TouchableOpacity>
          ))}
        </View>
      )}

      {/* Créer une nouvelle stratégie */}
      <View style={styles.section}>
        {!isCreating ? (
          <TouchableOpacity
            style={styles.createButton}
            onPress={() => setIsCreating(true)}
          >
            <Ionicons name="add-circle" size={24} color="#64ffda" />
            <Text style={styles.createButtonText}>Créer une stratégie personnalisée</Text>
          </TouchableOpacity>
        ) : (
          <View style={styles.createForm}>
            <Text style={styles.formTitle}>Nouvelle stratégie</Text>

            <TextInput
              style={styles.input}
              placeholder="Nom de la stratégie"
              placeholderTextColor="#666"
              value={newStrategyName}
              onChangeText={setNewStrategyName}
            />

            <View style={styles.inputRow}>
              <Text style={styles.label}>Rendement cible (%)</Text>
              <TextInput
                style={styles.smallInput}
                value={targetReturn}
                onChangeText={setTargetReturn}
                keyboardType="numeric"
                placeholderTextColor="#666"
              />
            </View>

            <View style={styles.inputRow}>
              <Text style={styles.label}>Volatilité max (%)</Text>
              <TextInput
                style={styles.smallInput}
                value={maxVolatility}
                onChangeText={setMaxVolatility}
                keyboardType="numeric"
                placeholderTextColor="#666"
              />
            </View>

            <View style={styles.riskSelector}>
              {(['conservative', 'moderate', 'aggressive'] as const).map((profile) => (
                <TouchableOpacity
                  key={profile}
                  style={[
                    styles.riskOption,
                    riskProfile === profile && { borderColor: getRiskColor(profile) },
                  ]}
                  onPress={() => setRiskProfile(profile)}
                >
                  <Ionicons
                    name={getRiskIcon(profile) as any}
                    size={20}
                    color={getRiskColor(profile)}
                  />
                </TouchableOpacity>
              ))}
            </View>

            <View style={styles.formButtons}>
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() => setIsCreating(false)}
              >
                <Text style={styles.cancelButtonText}>Annuler</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.saveButton}
                onPress={handleCreateStrategy}
              >
                <Text style={styles.saveButtonText}>Enregistrer</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>

      {/* Info théorique */}
      <View style={styles.infoBox}>
        <Ionicons name="information-circle" size={20} color="#64ffda" />
        <Text style={styles.infoText}>
          Le profil de risque détermine les contraintes appliquées lors de l'optimisation 
          du portefeuille selon le modèle de Markowitz.
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#16213e',
  },
  header: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ccd6f6',
  },
  subtitle: {
    fontSize: 14,
    color: '#8892b0',
    marginTop: 4,
  },
  section: {
    margin: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#e94560',
    marginBottom: 12,
    marginLeft: 4,
  },
  strategyCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  activeCard: {
    borderColor: '#e94560',
  },
  strategyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  strategyName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ccd6f6',
    marginLeft: 10,
  },
  strategyDescription: {
    color: '#8892b0',
    fontSize: 13,
    marginBottom: 8,
  },
  strategyDetails: {
    flexDirection: 'row',
    gap: 16,
  },
  detailText: {
    color: '#64ffda',
    fontSize: 12,
    fontFamily: 'monospace',
  },
  createButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderColor: '#2d3a5a',
    borderStyle: 'dashed',
  },
  createButtonText: {
    color: '#64ffda',
    marginLeft: 10,
    fontSize: 14,
  },
  createForm: {
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 16,
  },
  formTitle: {
    color: '#ccd6f6',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  input: {
    backgroundColor: '#0f0f23',
    borderRadius: 8,
    padding: 14,
    color: '#fff',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#2d3a5a',
  },
  inputRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  label: {
    color: '#ccd6f6',
    fontSize: 14,
  },
  smallInput: {
    backgroundColor: '#0f0f23',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: '#fff',
    width: 80,
    textAlign: 'right',
    borderWidth: 1,
    borderColor: '#2d3a5a',
  },
  riskSelector: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
    marginVertical: 16,
  },
  riskOption: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#0f0f23',
    borderWidth: 2,
    borderColor: '#2d3a5a',
  },
  formButtons: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 8,
  },
  cancelButton: {
    flex: 1,
    padding: 14,
    borderRadius: 8,
    backgroundColor: '#2d3a5a',
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#8892b0',
  },
  saveButton: {
    flex: 1,
    padding: 14,
    borderRadius: 8,
    backgroundColor: '#e94560',
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: '#0f3460',
    margin: 20,
    padding: 16,
    borderRadius: 12,
    marginBottom: 40,
  },
  infoText: {
    color: '#8892b0',
    fontSize: 12,
    marginLeft: 10,
    flex: 1,
    lineHeight: 18,
  },
});
