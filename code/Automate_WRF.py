from datetime import datetime  
from datetime import timedelta
from datetime import date

file_list = open('_namelist_file.txt', 'w').close()
file_list = open('_namelist_file.txt', 'w+')

start_threshold = datetime(2016, 1, 1)
end_threshold = datetime(2016, 1, 8)

end_date = end_threshold + timedelta(days=1)
start_date = end_date - timedelta(days=2)

count = 0

while start_date >= start_threshold:
    
    file = open("_namelist_wrf_"+start_date.strftime("%Y")+'-'+start_date.strftime("%m")+'-'+start_date.strftime("%d")+".txt", "w+")
    file_list.write("_namelist_wrf_"+start_date.strftime("%Y")+'-'+start_date.strftime("%m")+'-'+start_date.strftime("%d")+".txt\n")

    end_date_year = end_date.strftime("%Y")+  ', '+end_date.strftime("%Y")+ ',\n'
    end_date_month = end_date.strftime("%m")+ ', '+end_date.strftime("%m")+ ',\n'
    end_date_day = end_date.strftime("%d")+ ', '+end_date.strftime("%d")+ ',\n'

    start_date_year = start_date.strftime("%Y")+', '+start_date.strftime("%Y")+ ',\n'
    start_date_month = start_date.strftime("%m")+ ', '+start_date.strftime("%m")+ ',\n'
    start_date_day = start_date.strftime("%d")+ ', '+start_date.strftime("%d")+ ',\n'
    
    print(start_date.strftime("%Y")+'_'+start_date.strftime("%m")+'_'+start_date.strftime("%d")+' - '+end_date.strftime("%Y")+'_'+end_date.strftime("%m")+'_'+end_date.strftime("%d"))

    text_block_1 = ''' &time_control
    run_days                            = 2,
    run_hours                           = 00,
    run_minutes                         = 0,
    run_seconds                         = 0,
    start_year                          = '''
    text_block_2='''    start_month                         = '''
    text_block_3='''    start_day                           = '''
    text_block_4='''    start_hour                          = 00,   00,
    start_minute                        = 00,   00,
    start_second                        = 00,   00,
    end_year                            = '''
    text_block_5='''    end_month                           = '''
    text_block_6='''    end_day                             = '''
    text_block_7='''    end_hour                            = 00,   00,
    end_minute                          = 00,   00,
    end_second                          = 00,   00,
    interval_seconds                    = 21600
    input_from_file                     = .true.,.true.,
    history_interval                    = 5,   5,
    frames_per_outfile                  = 1000, 1000,
    restart                             = .false.,
    restart_interval                    = 5000,
    io_form_history                     = 2
    io_form_restart                     = 2
    io_form_input                       = 2
    io_form_boundary                    = 2
    debug_level                         = 0
    /

    &domains
    time_step                           = 24,
    time_step_fract_num                 = 0,
    time_step_fract_den                 = 10,
    max_dom                             = 2,
    e_we                                = 125,    124,
    e_sn                                = 125,    124,
    e_vert                              = 30,    30,
    p_top_requested                     = 10000,
    num_metgrid_levels                  = 40,
    num_metgrid_soil_levels             = 4,
    dx                                  = 4000, 1333.333,
    dy                                  = 4000, 1333.333,
    grid_id                             = 1,     2,
    parent_id                           = 0,     1,
    i_parent_start                      = 1,     42,
    j_parent_start                      = 1,     42,
    parent_grid_ratio                   = 1,     3,
    parent_time_step_ratio              = 1,     3,
    feedback                            = 1,
    smooth_option                       = 0
    /

    &physics
    physics_suite                       = 'CONUS'
    cu_physics                          = 0,     0,
    radt                                = 5,     5,
    bldt                                = 0,     0,
    cudt                                = 5,     5,
    icloud                              = 1,
    num_soil_layers                     = 4,
    num_land_cat                        = 21,
    sf_urban_physics                    = 0,     0,
    /

    &fdda
    /

    &dynamics
    w_damping                           = 0,
    diff_opt                            = 1,      1,
    km_opt                              = 4,      4,
    diff_6th_opt                        = 0,      0,
    diff_6th_factor                     = 0.12,   0.12,
    base_temp                           = 290.
    damp_opt                            = 0,
    zdamp                               = 5000.,  5000.,
    dampcoef                            = 0.2,    0.2,
    khdif                               = 0,      0,
    kvdif                               = 0,      0,
    non_hydrostatic                     = .true., .true.,
    moist_adv_opt                       = 1,      1,     
    scalar_adv_opt                      = 1,      1,    
    gwd_opt                             = 1,
    /

    &bdy_control
    spec_bdy_width                      = 5,
    spec_zone                           = 1,
    relax_zone                          = 4,
    specified                           = .true., .false.,
    nested                              = .false., .true.,
    /

    &grib2
    /

    &namelist_quilt
    nio_tasks_per_group = 0,
    nio_groups = 1,
    /'''

    text = text_block_1 + start_date_year + text_block_2 + start_date_month + text_block_3 + start_date_day + text_block_4 + end_date_year + text_block_5 + end_date_month + text_block_6 + end_date_day + text_block_7
    file.write(text)
    file.close()

    if count == 0:
        count = 1
        file_namelist = open('namelist.input', 'w').close()
        file_namelist = open('namelist.input', 'w+')
        file_namelist.write(text)
        file_namelist.close()

    start_date = start_date - timedelta(days=1)
    end_date = start_date + timedelta(days=2)
file_list.close()
