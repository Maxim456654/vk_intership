box.cfg{
    listen = 3301,  
   }

if not box.space.kv_store then
    local kv_store = box.schema.space.create('kv_store')
    kv_store:create_index('primary', { type = 'hash', parts = {1, 'string'} })
end

print("Tarantool initialization complete.")
