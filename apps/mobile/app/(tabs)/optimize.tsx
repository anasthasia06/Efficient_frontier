import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Switch,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { useOptimizationStore } from '@/store';
import {
  optimizePortfolio,
  calculatePortfolioMetrics,
} from '@/services/optimization';

const screenWidth = Dimensions.get('window').width;

/**
 * Écran d'optimisation de portefeuille
 * Implémentation de l'algorithme de Markowitz (Points 7-10 du document)
 */
export default function OptimizeScreen() {
  const {
    constraints,
    setConstraints,
    frontier,
    setFrontier,
    selectedPoint,
    selectPoint,
    isOptimizing,
    setOptimizing,
  } = useOptimizationStore();

  const [targetReturn, setTargetReturn] = useState('8');
  const [riskFreeRate, setRiskFreeRate] = useState('2');

  // Données synthétiques de démonstration (3 actifs)
  const demoAssets = {
    names: ['Actions FR', 'Obligations EU', 'Immobilier'],
    expectedReturns: [0.10, 0.04, 0.07], // 10%, 4%, 7%
    covMatrix: [
      [0.04, 0.006, 0.012],   // Variances et covariances
      [0.006, 0.01, 0.004],
      [0.012, 0.004, 0.025],
    ],
  };

  const handleOptimize = async () => {
    setOptimizing(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 500)); // Simulation

      const result = optimizePortfolio(
        demoAssets.expectedReturns,
        demoAssets.covMatrix,
        {
          ...constraints,
          targetReturn: parseFloat(targetReturn) / 100,
          riskFreeRate: parseFloat(riskFreeRate) / 100,
        }
      );

      setFrontier(result);
      selectPoint(null);
    } catch (error) {
      console.error('Erreur optimisation:', error);
    } finally {
      setOptimizing(false);
    }
  };

  // Préparer les données pour le graphique
  const chartData = frontier
    ? {
        labels: frontier.points.slice(0, 10).map((p) => (p.portfolioRisk * 100).toFixed(1)),
        datasets: [
          {
            data: frontier.points.slice(0, 10).map((p) => p.portfolioReturn * 100),
            color: (opacity = 1) => `rgba(233, 69, 96, ${opacity})`,
            strokeWidth: 2,
          },
        ],
      }
    : null;

  const chartConfig = {
    backgroundGradientFrom: '#1a1a2e',
    backgroundGradientTo: '#1a1a2e',
    decimalPlaces: 1,
    color: (opacity = 1) => `rgba(100, 255, 218, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(204, 214, 246, ${opacity})`,
    style: { borderRadius: 16 },
    propsForDots: {
      r: '5',
      strokeWidth: '2',
      stroke: '#64ffda',
    },
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Optimisation Markowitz</Text>
        <Text style={styles.subtitle}>Frontière efficiente μ-σ</Text>
      </View>

      {/* Paramètres de contraintes */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contraintes</Text>

        <View style={styles.inputRow}>
          <Text style={styles.label}>Rendement cible (r*)</Text>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              value={targetReturn}
              onChangeText={setTargetReturn}
              keyboardType="numeric"
              placeholder="8"
              placeholderTextColor="#666"
            />
            <Text style={styles.unit}>%</Text>
          </View>
        </View>

        <View style={styles.inputRow}>
          <Text style={styles.label}>Taux sans risque (r_f)</Text>
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              value={riskFreeRate}
              onChangeText={setRiskFreeRate}
              keyboardType="numeric"
              placeholder="2"
              placeholderTextColor="#666"
            />
            <Text style={styles.unit}>%</Text>
          </View>
        </View>

        <View style={styles.switchRow}>
          <Text style={styles.label}>Ventes à découvert</Text>
          <Switch
            value={constraints.allowShortSelling}
            onValueChange={(value) => setConstraints({ allowShortSelling: value })}
            trackColor={{ false: '#3e3e3e', true: '#e94560' }}
            thumbColor={constraints.allowShortSelling ? '#fff' : '#888'}
          />
        </View>
      </View>

      {/* Bouton d'optimisation */}
      <TouchableOpacity
        style={[styles.optimizeButton, isOptimizing && styles.buttonDisabled]}
        onPress={handleOptimize}
        disabled={isOptimizing}
      >
        {isOptimizing ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Calculer la frontière efficiente</Text>
        )}
      </TouchableOpacity>

      {/* Résultats */}
      {frontier && (
        <>
          {/* Graphique de la frontière */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Frontière Efficiente</Text>
            <Text style={styles.axisLabel}>Rendement μ (%) vs Risque σ (%)</Text>
            {chartData && (
              <LineChart
                data={chartData}
                width={screenWidth - 40}
                height={220}
                chartConfig={chartConfig}
                bezier
                style={styles.chart}
                onDataPointClick={({ index }) => selectPoint(index)}
              />
            )}
          </View>

          {/* Portefeuilles optimaux */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Portefeuilles Optimaux</Text>

            <View style={styles.optimalCard}>
              <Text style={styles.cardTitle}>Variance Minimale</Text>
              <View style={styles.cardRow}>
                <Text style={styles.cardLabel}>μ_p:</Text>
                <Text style={styles.cardValue}>
                  {(frontier.minVariancePortfolio.portfolioReturn * 100).toFixed(2)}%
                </Text>
              </View>
              <View style={styles.cardRow}>
                <Text style={styles.cardLabel}>σ_p:</Text>
                <Text style={styles.cardValue}>
                  {(frontier.minVariancePortfolio.portfolioRisk * 100).toFixed(2)}%
                </Text>
              </View>
              <View style={styles.weightsContainer}>
                {frontier.minVariancePortfolio.weights.map((w, i) => (
                  <Text key={i} style={styles.weight}>
                    {demoAssets.names[i]}: {(w * 100).toFixed(1)}%
                  </Text>
                ))}
              </View>
            </View>

            <View style={[styles.optimalCard, styles.sharpeCard]}>
              <Text style={styles.cardTitle}>Max Sharpe (Tangent)</Text>
              <View style={styles.cardRow}>
                <Text style={styles.cardLabel}>Sharpe:</Text>
                <Text style={styles.cardValueHighlight}>
                  {frontier.maxSharpePortfolio.sharpeRatio.toFixed(3)}
                </Text>
              </View>
              <View style={styles.cardRow}>
                <Text style={styles.cardLabel}>μ_p:</Text>
                <Text style={styles.cardValue}>
                  {(frontier.maxSharpePortfolio.portfolioReturn * 100).toFixed(2)}%
                </Text>
              </View>
              <View style={styles.cardRow}>
                <Text style={styles.cardLabel}>σ_p:</Text>
                <Text style={styles.cardValue}>
                  {(frontier.maxSharpePortfolio.portfolioRisk * 100).toFixed(2)}%
                </Text>
              </View>
              <View style={styles.weightsContainer}>
                {frontier.maxSharpePortfolio.weights.map((w, i) => (
                  <Text key={i} style={styles.weight}>
                    {demoAssets.names[i]}: {(w * 100).toFixed(1)}%
                  </Text>
                ))}
              </View>
            </View>
          </View>
        </>
      )}

      {/* Théorie */}
      <View style={styles.theorySection}>
        <Text style={styles.theoryTitle}>Formulation mathématique</Text>
        <Text style={styles.theory}>
          min w'Σw  s.t.  w'μ = r*, Σw_i = 1
        </Text>
        <Text style={styles.theoryNote}>
          où Σ est la matrice de covariance et μ le vecteur des rendements espérés.
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
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    margin: 10,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#e94560',
    marginBottom: 16,
  },
  inputRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  switchRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  label: {
    color: '#ccd6f6',
    fontSize: 14,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  input: {
    backgroundColor: '#0f0f23',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 8,
    color: '#fff',
    width: 80,
    textAlign: 'right',
    borderWidth: 1,
    borderColor: '#2d3a5a',
  },
  unit: {
    color: '#8892b0',
    marginLeft: 8,
  },
  optimizeButton: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    padding: 16,
    margin: 20,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  axisLabel: {
    color: '#8892b0',
    fontSize: 12,
    textAlign: 'center',
    marginBottom: 10,
  },
  chart: {
    borderRadius: 16,
    alignSelf: 'center',
  },
  optimalCard: {
    backgroundColor: '#0f0f23',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#64ffda',
  },
  sharpeCard: {
    borderLeftColor: '#e94560',
  },
  cardTitle: {
    color: '#ccd6f6',
    fontWeight: 'bold',
    marginBottom: 12,
  },
  cardRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  cardLabel: {
    color: '#8892b0',
  },
  cardValue: {
    color: '#64ffda',
    fontWeight: '600',
  },
  cardValueHighlight: {
    color: '#e94560',
    fontWeight: 'bold',
    fontSize: 18,
  },
  weightsContainer: {
    marginTop: 12,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  weight: {
    color: '#ccd6f6',
    fontSize: 12,
    backgroundColor: '#2d3a5a',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginRight: 8,
    marginBottom: 4,
  },
  theorySection: {
    padding: 20,
    marginBottom: 40,
  },
  theoryTitle: {
    color: '#8892b0',
    fontSize: 12,
    marginBottom: 8,
  },
  theory: {
    color: '#64ffda',
    fontFamily: 'monospace',
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 8,
  },
  theoryNote: {
    color: '#5a6785',
    fontSize: 11,
    textAlign: 'center',
  },
});
