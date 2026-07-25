/**
 * Durable Object for Task Queue Management
 * Manages video generation tasks and their status
 */

export class TaskQueue {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.tasks = new Map();
  }

  async fetch(request) {
    const url = new URL(request.url);
    const method = request.method;
    const path = url.pathname;

    if (method === 'GET' && path === '/status') {
      return this.getStatus(request);
    } else if (method === 'POST' && path === '/task') {
      return this.createTask(request);
    } else if (method === 'PUT' && path.startsWith('/task/')) {
      return this.updateTask(request);
    }

    return new Response('Not found', { status: 404 });
  }

  async getStatus(request) {
    const tasks = Array.from(this.tasks.values());
    return new Response(JSON.stringify({
      total: tasks.length,
      tasks: tasks
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  async createTask(request) {
    const { taskId, title, content } = await request.json();
    
    const task = {
      id: taskId,
      title: title,
      status: 'processing',
      progress: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.tasks.set(taskId, task);
    
    // Persist to storage
    await this.state.storage.put(`task:${taskId}`, JSON.stringify(task));

    return new Response(JSON.stringify(task), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  async updateTask(request) {
    const taskId = request.url.split('/').pop();
    const update = await request.json();

    const task = this.tasks.get(taskId);
    if (!task) {
      return new Response(JSON.stringify({ error: 'Task not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Update task
    Object.assign(task, update, { updatedAt: new Date().toISOString() });
    this.tasks.set(taskId, task);
    
    // Persist update
    await this.state.storage.put(`task:${taskId}`, JSON.stringify(task));

    return new Response(JSON.stringify(task), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
