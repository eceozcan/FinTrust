export interface ExpenseData {
    description: string;
    amount: number;
    currency: string;
    wallet: string;
}

export interface ExpenseResponse {
    category: string;
    suggestion: string;
    txid: string;
    explorer: string;
    amount: number;
    currency: string;
    amount_tl: number;
    error?: string;
}
