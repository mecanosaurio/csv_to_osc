library(taskscheduleR)
taskscheduler_create(taskname = "getting_sismos", rscript = "E:/SKETCHBOOK/python/utils/getSismos.R",
                     schedule = "MINUTE", starttime = "00:00", modifier = 2)

#ts <- taskscheduler_ls()
#tt <- ts$"Nombre de tarea"[3]
#tt
#[1] "getting_sismos"
#taskscheduler_delete(taskname=tt)
