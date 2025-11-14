export interface RecipeStep {
  id: string;
  raw_text: string;
  label: string;
  type: 'prep' | 'cook' | 'finish';
  duration_min: number;
  start_min: number;
  end_min: number;
  requires: string[];
  can_overlap_with: string[];
  equipment: string[];
  temperature_c?: number;
  notes: string;
}

export interface Recipe {
  id: string;
  title: string;
  source_url: string;
  week_label?: string;
  category?: string;
  ingredients: string[];
  nutrition?: {
    calories?: number;
    protein_g?: number;
    fat_g?: number;
    carbs_g?: number;
    fibre_g?: number;
    salt_g?: number;
  };
  steps: RecipeStep[];
  total_time_min: number;
  active_time_min: number;
}
