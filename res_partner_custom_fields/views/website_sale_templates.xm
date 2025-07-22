<odoo>
    <template id="custom_address_fields" inherit_id="website_sale.address">
        <xpath expr="//div[@id='div_name']" position="after">
            <div class="form-group">
                <label for="nombre">Nome</label>
                <input type="text" name="nombre" class="form-control" t-att-value="partner.nombre" required="required"/>
            </div>
            <div class="form-group">
                <label for="apellido">Apelido</label>
                <input type="text" name="apellido" class="form-control" t-att-value="partner.apellido" required="required"/>
            </div>
            <div class="form-group">
                <label for="dni">DNI</label>
                <input type="text" name="dni" class="form-control" t-att-value="partner.dni" required="required"/>
            </div>
        </xpath>
    </template>
</odoo>
