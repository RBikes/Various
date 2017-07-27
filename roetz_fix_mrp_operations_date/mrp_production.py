# coding: utf-8
from openerp.osv import fields
from openerp.osv import osv
import time
from datetime import datetime
from openerp.tools.translate import _


class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    def _compute_planned_workcenter(self, cr, uid, ids, context=None, mini=False):
        """ Computes planned and finished dates for work order.
        @return: Calculated date
        """
        dt_end = datetime.now()
        if context is None:
            context = {}
        for po in self.browse(cr, uid, ids, context=context):
            if po.date_planned:
                dt_end = datetime.strptime(po.date_planned, '%Y-%m-%d')
            else:
                po.date_planned = datetime.now()
            if not po.date_start:
                self.write(cr, uid, [po.id], {
                    'date_start': po.date_planned
                }, context=context, update=False)
            old = None
            for wci in range(len(po.workcenter_lines)):
                wc  = po.workcenter_lines[wci]
                if (old is None) or (wc.sequence>old):
                    dt = dt_end
                if context.get('__last_update'):
                    del context['__last_update']
                if (wc.date_planned < dt.strftime('%Y-%m-%d %H:%M:%S')) or mini:
                    self.pool.get('mrp.production.workcenter.line').write(cr, uid, [wc.id],  {
                        'date_planned': dt.strftime('%Y-%m-%d %H:%M:%S')
                    }, context=context, update=False)
                    i = self.pool.get('resource.calendar').interval_get(
                        cr,
                        uid,
                        #passing False makes resource_resource._schedule_hours run 1000 iterations doing nothing
                        wc.workcenter_id.calendar_id and wc.workcenter_id.calendar_id.id or None,
                        dt,
                        wc.hour or 0.0
                    )
                    if i:
                        dt_end = max(dt_end, i[-1][1])
                else:
                    if wc.date_planned_end:
                        dt_end = datetime.strptime(wc.date_planned_end, '%Y-%m-%d %H:%M:%S')

                old = wc.sequence or 0
            super(mrp_production, self).write(cr, uid, [po.id], {
                'date_finished': dt_end
            })
            return dt_end

