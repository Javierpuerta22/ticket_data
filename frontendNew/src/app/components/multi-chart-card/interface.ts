export interface dataChart {
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string | string[];
    borderWidth?: number;
}

export interface MultiChartCardProps {
    datasets: dataChart[];
    labels: string[];
    title: string;
    type: string;
    options?: any;
}