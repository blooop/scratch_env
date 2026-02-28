import { Recipe } from './types';
import recipesData from '../../data/recipes_with_schedule.json';

export function getRecipes(): Recipe[] {
  return recipesData as Recipe[];
}

export function getRecipeById(id: string): Recipe | undefined {
  const recipes = getRecipes();
  return recipes.find(recipe => recipe.id === id);
}

export function getWeeks(): string[] {
  const recipes = getRecipes();
  const weeks = new Set<string>();

  recipes.forEach(recipe => {
    if (recipe.week_label) {
      weeks.add(recipe.week_label);
    }
  });

  return Array.from(weeks).sort().reverse(); // Most recent first
}

export function getRecipesByWeek(weekLabel: string): Recipe[] {
  const recipes = getRecipes();
  return recipes.filter(recipe => recipe.week_label === weekLabel);
}

export function getLatestWeek(): string | null {
  const weeks = getWeeks();
  return weeks.length > 0 ? weeks[0] : null;
}
