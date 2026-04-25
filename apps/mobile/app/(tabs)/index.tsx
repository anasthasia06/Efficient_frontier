import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
} from 'react-native';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { useAuthStore, usePortfolioStore } from '@/store';

const screenWidth = Dimensions.get('window').width;

/**
 * Dashboard principal - Vue d'ensemble du portefeuille
 */
export default function DashboardScreen() {
  const { user } = useAuthStore();
  const { currentPortfolio } = usePortfolioStore();

  // Données de démonstration
  const demoAllocation = [
    { name: 'Actions', population: 45, color: '#e94560', legendFontColor: '#ccd6f6' },
    { name: 'Obligations', population: 30, color: '#0f3460', legendFontColor: '#ccd6f6' },
    { name: 'Immobilier', population: 15, color: '#533483', legendFontColor: '#ccd6f6' },
    { name: 'Liquidités', population: 10, color: '#64ffda', legendFontColor: '#ccd6f6' },
  ];

  const demoPerformance = {
    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
    datasets: [
      {
        data: [100, 102.5, 101.8, 105.2, 108.1, 110.5],
        color: (opacity = 1) => `rgba(233, 69, 96, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  const chartConfig = {
    backgroundGradientFrom: '#1a1a2e',
    backgroundGradientTo: '#1a1a2e',
    decimalPlaces: 1,
    color: (opacity = 1) => `rgba(100, 255, 218, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(204, 214, 246, ${opacity})`,
    style: { borderRadius: 16 },
    propsForDots: {
      r: '4',
      strokeWidth: '2',
      stroke: '#e94560',
    },
  };

  return (
    <ScrollView style={styles.container}>
      {/* En-tête */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Bonjour, {user?.name || 'Gestionnaire'}</Text>
        <Text style={styles.date}>{new Date().toLocaleDateString('fr-FR', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}</Text>
      </View>

      {/* Métriques clés */}
      <View style={styles.metricsContainer}>
        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Rendement Espéré</Text>
          <Text style={styles.metricValue}>8.5%</Text>
          <Text style={styles.metricUnit}>μ_p annualisé</Text>
        </View>
        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Volatilité</Text>
          <Text style={styles.metricValue}>12.3%</Text>
          <Text style={styles.metricUnit}>σ_p annualisé</Text>
        </View>
        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Ratio de Sharpe</Text>
          <Text style={[styles.metricValue, styles.sharpeValue]}>0.69</Text>
          <Text style={styles.metricUnit}>(μ-r_f)/σ</Text>
        </View>
      </View>

      {/* Graphique de performance */}
      <View style={styles.chartSection}>
        <Text style={styles.sectionTitle}>Performance du Portefeuille</Text>
        <LineChart
          data={demoPerformance}
          width={screenWidth - 40}
          height={200}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </View>

      {/* Allocation */}
      <View style={styles.chartSection}>
        <Text style={styles.sectionTitle}>Allocation Actuelle</Text>
        <PieChart
          data={demoAllocation}
          width={screenWidth - 40}
          height={200}
          chartConfig={chartConfig}
          accessor="population"
          backgroundColor="transparent"
          paddingLeft="15"
          absolute
        />
      </View>

      {/* Indicateurs de risque */}
      <View style={styles.riskSection}>
        <Text style={styles.sectionTitle}>Indicateurs de Risque</Text>
        <View style={styles.riskGrid}>
          <View style={styles.riskItem}>
            <Text style={styles.riskLabel}>VaR 95%</Text>
            <Text style={styles.riskValue}>-4.2%</Text>
          </View>
          <View style={styles.riskItem}>
            <Text style={styles.riskLabel}>CVaR</Text>
            <Text style={styles.riskValue}>-5.8%</Text>
          </View>
          <View style={styles.riskItem}>
            <Text style={styles.riskLabel}>Max Drawdown</Text>
            <Text style={styles.riskValue}>-8.1%</Text>
          </View>
          <View style={styles.riskItem}>
            <Text style={styles.riskLabel}>Beta</Text>
            <Text style={styles.riskValue}>0.85</Text>
          </View>
        </View>
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
    paddingTop: 10,
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ccd6f6',
  },
  date: {
    fontSize: 14,
    color: '#8892b0',
    marginTop: 4,
  },
  metricsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 10,
    marginBottom: 20,
  },
  metricCard: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 11,
    color: '#8892b0',
    marginBottom: 8,
  },
  metricValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#64ffda',
  },
  sharpeValue: {
    color: '#e94560',
  },
  metricUnit: {
    fontSize: 10,
    color: '#5a6785',
    marginTop: 4,
  },
  chartSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#ccd6f6',
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
  riskSection: {
    padding: 20,
    paddingBottom: 40,
  },
  riskGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  riskItem: {
    width: '50%',
    padding: 10,
  },
  riskLabel: {
    fontSize: 12,
    color: '#8892b0',
  },
  riskValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ff6b6b',
    marginTop: 4,
  },
});
