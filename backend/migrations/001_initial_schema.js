/** @param {import('knex').Knex} knex */
export async function up(knex) {
  await knex.schema.createTable('users', (t) => {
    t.increments('id').primary();
    t.string('email').notNullable().unique();
    t.string('password_hash').notNullable();
    t.string('name').notNullable();
    t.integer('height_cm');
    t.float('weight_kg');
    t.integer('age');
    t.string('gender');
    t.string('ethnicity');
    t.jsonb('diet_restrictions').defaultTo('[]');
    t.timestamps(true, true);
  });

  await knex.schema.createTable('foods', (t) => {
    t.increments('id').primary();
    t.string('name').notNullable();
    t.jsonb('nutrients').notNullable();
    t.timestamps(true, true);
  });

  await knex.schema.createTable('meals', (t) => {
    t.increments('id').primary();
    t.integer('user_id').references('id').inTable('users').onDelete('CASCADE');
    t.timestamp('consumed_at').notNullable().defaultTo(knex.fn.now());
    t.jsonb('items').notNullable();
    t.integer('total_calories').defaultTo(0);
    t.timestamps(true, true);
  });

  await knex.schema.createTable('recipes', (t) => {
    t.increments('id').primary();
    t.string('name').notNullable();
    t.jsonb('ingredients').notNullable();
    t.timestamps(true, true);
  });

  await knex.schema.createTable('user_diet_logs', (t) => {
    t.increments('id').primary();
    t.integer('user_id').references('id').inTable('users').onDelete('CASCADE');
    t.date('day').notNullable();
    t.integer('calories').defaultTo(0);
    t.jsonb('macros').defaultTo('{}');
    t.jsonb('micros').defaultTo('{}');
    t.unique(['user_id', 'day']);
    t.timestamps(true, true);
  });
}

/** @param {import('knex').Knex} knex */
export async function down(knex) {
  await knex.schema.dropTableIfExists('user_diet_logs');
  await knex.schema.dropTableIfExists('recipes');
  await knex.schema.dropTableIfExists('meals');
  await knex.schema.dropTableIfExists('foods');
  await knex.schema.dropTableIfExists('users');
}
