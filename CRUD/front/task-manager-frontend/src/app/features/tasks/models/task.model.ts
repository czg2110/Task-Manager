export interface Task {
  id?: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'on-review' | 'blocked';
  createdAt?: string;
  assignee?: string;
  startDate?: string;
  endDate?: string;
}